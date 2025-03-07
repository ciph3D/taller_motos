from odoo import models, fields, api, _

class Moto(models.Model):
    _name = 'taller.moto'
    _description = 'Motocicleta del cliente'
    _rec_name = 'display_name'

    # Campos básicos
    marca = fields.Char(string='Marca', required=True)
    modelo = fields.Char(string='Modelo', required=True)
    matricula = fields.Char(string='Matrícula', required=True)
    chasis = fields.Char(string='Nº Chasis')
    fecha_compra = fields.Date(string='Fecha de compra')
    kilometraje = fields.Float(string='Kilometraje')
    notas = fields.Text(string='Notas')
    
    # Campo para imagen
    imagen = fields.Binary(string='Imagen')
    
    # Relaciones
    cliente_id = fields.Many2one('res.partner', string='Cliente', required=True)
    
    # Estados
    state = fields.Selection([
        ('activa', 'Activa'),
        ('reparacion', 'En reparación'),
        ('baja', 'Baja')
    ], string='Estado', default='activa')
    
    # Campos calculados
    display_name = fields.Char(compute='_compute_display_name', store=True)
    repair_count = fields.Integer(compute='_compute_repair_count', string="Reparaciones")
    
    @api.depends('marca', 'modelo', 'matricula')
    def _compute_display_name(self):
        for moto in self:
            moto.display_name = f"{moto.marca} {moto.modelo} ({moto.matricula or 'Sin matrícula'})"
    
    @api.depends()
    def _compute_repair_count(self):
        for moto in self:
            moto.repair_count = self.env['project.project'].search_count([
                ('moto_id', '=', moto.id)
            ])
    
    def action_view_repairs(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Reparaciones'),
            'res_model': 'project.project',
            'view_mode': 'list,form',
            'domain': [('moto_id', '=', self.id)],
            'context': {'default_moto_id': self.id, 'default_partner_id': self.cliente_id.id}
        }