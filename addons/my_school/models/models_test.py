from odoo import api, models, fields
import random
from pygments.lexer import _inherit
from odoo.exceptions import ValidationError
i = 0;

class person_test(models.Model):
    _name = 'school.persontest'
    _description = 'Person test'
    _inherit = ['school.person']
    
    test1 = fields.Char(compute = '_get_test1', store=True)
    @api.depends('name')
    def _get_test1(self):
        self.test1 = f'{random.randint(0,10000)}'


    
    test_constrains = fields.Char()
    @api.constrains('test_constrains')
    def length_large(self):
        if self.test_constrains and len(self.test_constrains) >=5:
            print('heloo')
            # raise Exception("Test Exception")
            

    test_sql_constraints1 = fields.Char()
    test_sql_constraints2 = fields.Char()
    _sql_constraints = [
        ('test_check_1', 'CHECK(LENGTH(test_sql_constraints1) <= 5)', 'test_sql_constaints1 phải nhỏ hơn 5 kí tự'),
        ('test_check_2', 'CHECK(LENGTH(test_sql_constraints2) <= 10)', 'test_sql_constraints2 phải nhỏ hơn 10 kí tự')
    ]
    
    
    
    int_field = fields.Integer()
    @api.onchange('int_field')
    def int_change(self):
        if self.int_field >= 10:
            return {
                'warning': {
                    'title': "return of @api.constraint - Title",
                    'message': "Int field không được lớn hơn 10",
                },
            }
            
    
    
    
    user_id = fields.Many2one('res.users', default=lambda self:self.env.user)
    
    test_domain = fields.Many2one('school.student', string='Test attr domain in field Many2one',
                            domain=[('gioi_tinh', '=', 'Nu_')],
                            help='domain lọc học sinh hiển thị sẵn có trong many2one()')
    
    test_date = fields.Date(default = '2021-01-31')
    test_datetime = fields.Datetime(default = '2021-01-31 20:00:00')
    
  
    state = fields.Selection([
        ('su_dung', 'Sử dụng'), ('het_han', 'Hết hạn'), ('hong', 'Hỏng')
        ], default = 'su_dung')


    def click_button(self):
        print(self.name)
        raise ValidationError(f'{self.name}')
        return {'1':1}
        
    phan_quyen_field = fields.Char(groups = 'my_school.group_giao_vien')


    @api.constrains('name')
    def testv3(self):
        print('testv3: ',self.name)
        
    img_test = fields.Image()
    
    
    def test_v2(self):
        print('------------------------------------------------------------------------\n')
        print('self.name:     ', self.name)
        print('selef.user_id:   ',  self.user_id)
        for o in self.user_id:
            print(o, end="|")
        print('\n\n------------------------------------------------------------------------')

        
class test_xx(models.Model):
    _inherit = 'school.persontest'
    _description = 'test onchange ke thua'
    
    
    # Ghi đè onchange khi kế thừa model thì cái này sẽ chạy.
    @api.onchange('int_field') 
    def int_change(self):
        if self.int_field >=20:
            return {
                'warning': {
                    'title': "return of @api.constraint - Title",
                    'message': "Int field không được lớn hơn 20",
                },
            }
            
    # Tương tự như trên, connstrains của model sẽ chạy.
    @api.constrains('test_constrains')
    def test_override_constrains(self):
        if  self.test_constrains and len(self.test_constrains) >= 10:
            raise ValidationError('test_constrains length >= 10!!!!!!!')
        
    
    
    @staticmethod
    def run():
        from datetime import datetime
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        print('cron running: ', f'{random.randint(0,100)}')        


class LaoCong(models.Model):
    _name = 'school.laocong'
    _description = 'test thừa kế ủy thác'
    _inherits = {'school.person': 'person_id'}
    
    person_id = fields.Many2one('school.person')          
    level = fields.Char(string='Level Lao Công')

class BuoiHoc(models.Model):
    _name = 'school.test.buoihoc'
    _description = 'test buổi học'
    
    start_date = fields.Datetime(default='2021-01-20 20:20:20')
    end_date = fields.Datetime(default='2021-02-20 20:20:20')
    int_test = fields.Integer()
    name2 = fields.Char(default = 'name2 default')
    html_field = fields.Html()      
            
            
class test_wizards(models.TransientModel):
    _name = 'school.test.wizards'
    _description = "Test wizards"
    
    
    
    def _default_laocong(self):
        return self.env['school.laocong'].browse(self._context.get('active_id'))
    
    laocong_id = fields.Many2one('school.laocong', default=_default_laocong)
    level = fields.Char(default='test 12313')
    
    def subscribe(self):
        for o in self.laocong_id:
            o.level = self.level  
        return {}       
            
            
            
            
            
            
            
            
            
            
            
            
            