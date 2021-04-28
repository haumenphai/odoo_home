from datetime import date
from odoo import models, api, fields

PLAYER_RATING = [
    ('0', 'Not Rating'),
    ('1', 'Very Bad'),
    ('2', 'Bad'),
    ('3', 'Neutral'),
    ('4', 'Good'),
    ('5', 'Very Good'),
]


class Player(models.Model):
    _name = 'football.player'
    _description = 'Player'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    avatar = fields.Image(string='Avatar', max_width=128, max_height=200)
    name = fields.Char(string='Name', required=True)
    birthday = fields.Date(string='Birthday')
    age = fields.Char(string='Age', compute='_compute_age')
    phone_number = fields.Char(string='Phone Number')
    email = fields.Char(string='Email')
    player_position_ids = fields.Many2many('football.playerposition', string='Player Position', tracking=True)

    index_finish = fields.Float(string='Index Finish')
    speed = fields.Float(string='Index Speed')
    cam = fields.Float(string='Index Cam')
    power = fields.Float(string='Index Power')
    defense = fields.Float(string='Index Defense')

    general = fields.Float(string='General', compute='_compute_general_rate', store=True)
    rate = fields.Selection(PLAYER_RATING, compute='_compute_general_rate', string='Rating')

    _sql_constraints = [
        ('check_index_finish_vaild',
         'CHECK(index_finish <= 100 AND index_finish >= 0)',
         "Index Finish must be >= 0 and <= 100"),
        ('check_speed_vaild',
         'CHECK(speed <= 100 AND speed >= 0)',
         "Speed must be >= 0 and <= 100"),
        ('check_cam_vaild',
         'CHECK(cam <= 100 AND cam >= 0)',
         "Cam must be >= 0 and <= 100"),
        ('check_power_vaild',
         'CHECK(power <= 100 AND power >= 0)',
         "Power must be >= 0 and <= 100"),
        ('check_defense_vaild',
         'CHECK(defense <= 100 AND defense >= 0)',
         "Defense >= 0 and <= 100"),
    ]

    def write(self, vals):
        for r in self:
            position_old_ids = r.player_position_ids
            super(Player, r).write(vals)
            position_new_ids = r.player_position_ids

            if position_old_ids != position_new_ids:
                body = f"<b>Player Positon Has Changed From: </b>"
                for position in position_old_ids:
                    body += f"<a href=# data-oe-model=football.playerposition data-oe-id={position.id}>{position.name}</a>, "
                body = body[:len(body) - 2]
                body += "<b> To </b>"

                for position in position_new_ids:
                    body += f"<a href=# data-oe-model=football.playerposition data-oe-id={position.id}>{position.name}</a>, "
                body = body[:len(body) - 2]

                r.message_post(body=body)

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        return super(Player, self.with_context(mail_post_autofollow=True)).message_post(**kwargs)


    @api.depends('index_finish', 'speed', 'cam', 'power', 'general')
    def _compute_general_rate(self):
        for r in self:
            r.general = (r.index_finish + r.speed + r.cam + r.power + r.defense) / 5
            if r.general <= 20:
                r.rate = '1'
            elif 21 <= r.general <= 40:
                r.rate = '2'
            elif 41 <= r.general <= 60:
                r.rate = '3'
            elif 61 <= r.general <= 80:
                r.rate = '4'
            else:
                r.rate = '5'


    @api.depends('birthday')
    def _compute_age(self):
        for r in self:
            if r.birthday:
                r.age = self.calculate_age(r.birthday)
            else:
                r.age = ''

    def calculate_age(self, birthDate):
        today = date.today()
        age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
        return age
