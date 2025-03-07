# Archivo: models/moto.py
from odoo import models, fields, api

class Moto(models.Model):
    _name = 'taller.moto'
    _description = 'Motocicleta del cliente'

    name = fields.Char(string='Nombre', compute='_compute_name')
    marca = fields.Char(string='Marca', required=True)
    modelo = fields.Char(string='Modelo', required=True)
    matricula = fields.Char(string='Matrícula', required=True)
    fecha_compra = fields.Date(string='Fecha de compra')
    kilometraje = fields.Float(string='Kilometraje')
    state = fields.Selection([
        ('activa', 'Activa'),
        ('taller', 'En taller'),
        ('inactiva', 'Inactiva')
    ], string='Estado', default='activa')
    
    cliente_id = fields.Many2one('res.partner', string='Cliente', required=True)
    
    @api.depends('marca', 'modelo', 'matricula')
    def _compute_name(self):
        for moto in self:
            moto.name = f"{moto.marca} {moto.modelo} ({moto.matricula or 'Sin matrícula'})"

# Archivo: models/partner.py
from odoo import models, fields, api

class Partner(models.Model):
    _inherit = 'res.partner'
    
    moto_ids = fields.One2many('taller.moto', 'cliente_id', string='Motos')
    moto_count = fields.Integer(string='Número de motos', compute='_compute_moto_count')
    
    @api.depends('moto_ids')
    def _compute_moto_count(self):
        for partner in self:
            partner.moto_count = len(partner.moto_ids)
    
    def action_view_motos(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Motos del cliente',
            'res_model': 'taller.moto',
            'view_mode': 'tree,form',
            'domain': [('cliente_id', '=', self.id)],
            'context': {'default_cliente_id': self.id}
        }