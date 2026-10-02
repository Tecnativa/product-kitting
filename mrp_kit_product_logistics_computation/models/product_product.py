#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    # Fields overridden to make them computed, defined in the stock module.
    volume = fields.Float(
        compute="_compute_volume", store=True, readonly=False, recursive=True
    )
    weight = fields.Float(
        compute="_compute_weight", store=True, readonly=False, recursive=True
    )

    @api.depends(
        "bom_ids",
        "bom_ids.type",
        "bom_ids.bom_line_ids",
        "bom_ids.bom_line_ids.product_id",
        "bom_ids.bom_line_ids.product_qty",
        "bom_ids.bom_line_ids.product_id.volume",
    )
    def _compute_volume(self):
        # Calculates the kit's volume by summing the
        # volumes of its BoM components.
        if hasattr(super(), "_compute_volume"):
            super()._compute_volume()
        for product in self.filtered("is_kits"):
            bom_id = product.bom_ids.filtered(lambda bom: bom.type == "phantom")[:1]
            if bom_id:
                product.volume = sum(
                    [
                        bl.product_id.volume * bl.product_qty
                        for bl in bom_id[0].bom_line_ids
                    ]
                )
        return

    @api.depends(
        "bom_ids",
        "bom_ids.type",
        "bom_ids.bom_line_ids",
        "bom_ids.bom_line_ids.product_id",
        "bom_ids.bom_line_ids.product_qty",
        "bom_ids.bom_line_ids.product_id.weight",
    )
    def _compute_weight(self):
        # Calculates the kit's weight by summing the
        # weights of its BoM components.
        if hasattr(super(), "_compute_weight"):
            super()._compute_weight()
        for product in self.filtered("is_kits"):
            bom_id = product.bom_ids.filtered(lambda bom: bom.type == "phantom")[:1]
            if bom_id:
                product.weight = sum(
                    [
                        bl.product_id.weight * bl.product_qty
                        for bl in bom_id[0].bom_line_ids
                    ]
                )
        return
