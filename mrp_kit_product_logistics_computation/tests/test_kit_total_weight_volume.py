# Copyright 2026 Tecnativa - Adasat Torres
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import Command
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestKitTotalWeightVolume(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        ProductCategory = cls.env["product.category"]
        ProductProduct = cls.env["product.product"]
        MRPBom = cls.env["mrp.bom"]
        cls.product_category = ProductCategory.create(
            {
                "name": "Test category",
            }
        )
        cls.product1 = ProductProduct.create(
            {
                "name": "Test 1",
                "list_price": 100,
                "type": "consu",
                "categ_id": cls.product_category.id,
            }
        )
        cls.product2 = ProductProduct.create(
            {
                "name": "Test 2",
                "list_price": 100,
                "type": "consu",
                "categ_id": cls.product_category.id,
                "volume": 10,
                "weight": 10,
            }
        )
        cls.product3 = ProductProduct.create(
            {
                "name": "Test 2",
                "list_price": 100,
                "type": "consu",
                "categ_id": cls.product_category.id,
                "volume": 10,
                "weight": 10,
            }
        )
        cls.bom_id = MRPBom.create(
            {
                "product_tmpl_id": cls.product1.product_tmpl_id.id,
                "product_id": cls.product1.id,
                "type": "phantom",
                "bom_line_ids": [
                    Command.create({"product_id": cls.product2.id, "product_qty": 1.0}),
                    Command.create({"product_id": cls.product3.id, "product_qty": 2.0}),
                ],
            }
        )

    def test_product_weight_volume(self):
        self.assertEqual(self.product1.volume, 30)
        self.assertEqual(self.product1.weight, 30)
        self.product2.volume = 30
        self.product3.volume = 100
        self.assertEqual(self.product1.volume, 230)
        self.product2.weight = 15
        self.product3.weight = 50
        self.assertEqual(self.product1.weight, 115)
        self.product4 = self.env["product.product"].create(
            {
                "name": "Test 4",
                "type": "consu",
                "categ_id": self.product_category.id,
                "volume": 10,
                "weight": 10,
            }
        )
        self.bom_id.write(
            {
                "bom_line_ids": [
                    Command.create(
                        {"product_id": self.product4.id, "product_qty": 2.0}
                    ),
                ]
            }
        )
        self.assertEqual(self.product1.weight, 135)
        self.assertEqual(self.product1.volume, 250)
