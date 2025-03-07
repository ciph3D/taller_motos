# Opción 1: Añadir el campo "modelo" al modelo res.partner
# En tu archivo models/partner.py

from odoo import models, fields, api

class Partner(models.Model):
    _inherit = 'res.partner'
    
    modelo = fields.Char(string="Modelo", help="Campo de modelo para taller de motos")
    meeting_count = fields.Integer(string="Meetings", compute="_compute_meeting_count")
    
    @api.depends()
    def _compute_meeting_count(self):
        for partner in self:
            partner.meeting_count = self.env['calendar.event'].search_count([
                ('partner_ids', 'in', partner.id)
            ])
    
    def schedule_meeting(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Programar Reunión',
            'res_model': 'calendar.event',
            'view_mode': 'form',
            'context': {
                'default_partner_ids': [(6, 0, [self.id])],
            },
        }