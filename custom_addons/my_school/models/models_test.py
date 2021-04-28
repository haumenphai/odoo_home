from odoo import api, models, fields
import random
from odoo.exceptions import ValidationError

i = 0


class person_test(models.Model):
    _name = 'school.persontest'
    _description = 'Person test'
    _inherit = ['school.person']

    address = fields.Char(default="địa chỉ mặc định")

    test1 = fields.Char(compute='_get_test1', store=True)

    @api.depends('name')
    def _get_test1(self):
        self.test1 = f'{random.randint(0, 10000)}'

    test_constrains = fields.Char()

    @api.constrains('test_constrains')
    def length_large(self):
        if self.test_constrains and len(self.test_constrains) >= 5:
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

    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)

    test_domain = fields.Many2one('school.student', string='Test attr domain in field Many2one',
                                  domain=[('gioi_tinh', '=', 'Nu_')],
                                  help='domain lọc học sinh hiển thị sẵn có trong many2one()')

    test_date = fields.Date(default='2021-01-31')
    test_datetime = fields.Datetime(default='2021-01-31 20:00:00')
    related_field_test = fields.Char(related='test_domain.name', string="Related Field Test 'test_domain.name'",
                                     readonly=False)

    state = fields.Selection([
        ('su_dung', 'Sử dụng'), ('het_han', 'Hết hạn'), ('hong', 'Hỏng')
    ], default='su_dung')

    test_one2many = fields.One2many('school.giaovien', 'person_test_id')
    test_many2many = fields.Many2many('school.giaovien')

    def click_button(self):
        print(self.name)
        raise ValidationError(f'{self.name}')
        return {'1': 1}

    phan_quyen_field = fields.Char(groups='my_school.group_giao_vien')

    @api.constrains('name')
    def testv3(self):
        print('testv3: ', self.name)

    img_test = fields.Image()

    def view_init(self, fields_list):
        """ Override this method to do specific things when a form view is
        opened. This method is invoked by :meth:`~default_get`.
        """
        print('view init')

    def test_v2(self):
        print('------------------------------------------------------------------------\n')
        print('self.name:     ', self.name)
        print('selef.user_id:   ', self.user_id)
        for o in self.user_id:
            print(o, end="|")
        print('\n\n')
        print('field access: ', self['user_id']['name'])
        print('self.mapped(\'age\')', self.mapped('age'))
        # self['name'] = 'abc abc'
        print(self.env.ref('my_school.list_view_giao_vien')['name'])
        print(self.env.user['name'])
        print(self.env.company['name'])
        print(self.env.companies)
        # print(models.Model.with_user(self.env.user))
        print(models.check_object_name('res.useR'))
        print('self.default_get(): ', self.default_get('state'))
        print(self.fields_get_keys())
        # print(self.user_has_groups())
        records = self.search([('gioi_tinh', '=', 'Nam_')])
        for o in records:
            print('name: ', o.name)
        print('------------------------------------------------------------------------')

    def delete_person(self):  # Work
        self.unlink()

    def create_person(self):
        vals = [{
            'name': 'Person 1',
            'birth_day': '2020-10-10',
            'address': '  Đỉa chỉ m '
        }]

        self.create([{
            'name': 'Person 1',
            'birth_day': '2020-10-10',
            'address': '  Đỉa chỉ m '
        }])

    def copy_person(self):
        self.copy(default={'name': 'Person COpy'})



    # =============================#
    #      Test ORM Method        #
    # =============================#
    def test_wirte(self):
        # v = {'name': 'ggggg', 'address': 'gg', 'birth_day': '2020-12-12', 'gioi_tinh':'Nam_'}
        # 'test_many2many': (0, 0, })
        self.write({
            'name': 'Person --Wirte',
            'user_id': 1,
            'test_date': '2025-12-30',
            'test_datetime': '2025-12-30 12:30:00',

        })

    def test_browse(self):

        r = self.browse(31)
        print('browse: ', r.name)
        users = self.env['res.users'].browse([1, 2])

        for o in users:
            print(o.name)

    def test_exists(self):
        r1 = self.browse(100)
        if r1.exists():
            print('Ton Tai')

        print('self.exists', self.exists())

    def test_ref(self):
        r1 = self.env.ref('my_school.report_giao_vien1')
        print('ref: ', r1)

    def test_search(self):
        # Search theo domain, trả về recordset
        recordset = self.search([])
        print('recordset: ', recordset)

        r1 = self.search(args=[('name', '=', 'Person COpy')], limit=4, order='test_domain')
        print('r1: ', r1)

    def test_search_count(self):
        # Chỉ trả về số lượng tìm thấy.
        kq = self.search_count([('name', '=', 'Person COpy')])
        print('kq: ', kq)

    def test_name_search(self):
        # search theo name và domain.
        r1 = self.name_search(name='Person COpy', operator='=', args=[('name', '=', 'do2')])
        print('name_search', r1)

        for o in r1:
            print('a', o.name, o)

    def test_read(self):
        #Đọc giá trị các trường, return dict.
        l1 = self.read(['name', 'age'])
        print('l1', l1)

    def test_read_group(self):
        l1 = self.read_group(domain=[], fields=['name'], groupby=['name'])
        print('read_group: ', l1)

    def test_fields_get(self):
        # Lấy các thôn tin về thuộc tính của field (string, readonly, help,...
        # Trả về dict {'name': {string}, 'id': {string,}}
        s = self.fields_get(['name', 'id'], ['string'])
        print(s)

    def test_fields_view_get(self):
        # Lấy thông tin, thành phần chi tiết của view.
        s = self.fields_view_get(369)
        print(s)

    def test_unlink(self):
        self.unlink()


    def test_ham(self):
        # s = self.default_get(['name', 'age', 'gioi_tinh', 'birth_day'])
        # print(s)

        # print('=============================')
        #
        # s = self.name_create('Hello Person')
        # print('s: ', s)

        # self.write({'gioi_tinh': 'Nu_'})
        # print(self.env['school.2'])
        #
        # print(self._context)
        # r2 = self.with_context({}, uid=6)
        # print('r2:', r2._context)
        # r2.env['school.giaovien']

        # self.write({'name': 'new name123', 'gioi_tinh': 'Nam_'})

        # new_record = self.name_create(name='New Records123')
        # print(new_record)

        # self.test_wirte()
        # self.test_browse()
        # self.test_exists()
        # self.test_ref()
        # self.test_search()
        # self.test_search_count()
        # self.test_name_search()
        # self.test_read()
        # self.test_read_group()
        # self.test_fields_get()
        # self.test_fields_view_get()
        # self.unlink()
        # self.tesss1()
        # self.test_context()
        self.create([{'name': '123'},{'name': '1234'}])
        
    
    
    def test_context(self):
        # Context là 1 dict chứa thông tin về current user, lang, timezone, ...
        print('context: ', self.env.context)
        
    
    def test_with_user(self):
        # Có thể thay đổi user mới để tương tác, thay đổi quyền hạn.
        self.with_user(1).unlink()
        
    
    def tesss1(self):
        # Write chỉ thực hiện được trên 1 record.
        for r in self:
            r.write(vals={'name':'dohaumen', 'age':1000})
        
    
    def unlink(self):
        print('unlink')
        super(person_test, self).unlink()
    

class test_name_valid(models.Model):
    _name = 'school.2'
    a = 'a ====================132323123213'


class test_xx(models.Model):
    _inherit = 'school.persontest'
    _description = 'test onchange ke thua'

    # Ghi đè onchange khi kế thừa model thì cái này sẽ chạy.
    @api.onchange('int_field')
    def int_change(self):
        if self.int_field >= 20:
            return {
                'warning': {
                    'title': "return of @api.constraint - Title",
                    'message': "Int field không được lớn hơn 20",
                },
            }

    # Tương tự như trên, connstrains của model sẽ chạy.
    @api.constrains('test_constrains')
    def test_override_constrains(self):
        if self.test_constrains and len(self.test_constrains) >= 10:
            raise ValidationError('test_constrains length >= 10!!!!!!!')

    @staticmethod
    def run():
        from datetime import datetime
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        print('cron running: ', f'{random.randint(0, 100)}')


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
    name2 = fields.Char(default='name2 default')
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
