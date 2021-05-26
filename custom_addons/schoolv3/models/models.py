# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Student(models.Model):
    _name = 'schoolv3.student'
    _description = 'schoolv3.student'

    name = fields.Char(string='Name')
    age = fields.Integer(string='Age', default=20)
    address = fields.Char(string='Address', default='default address')

    state_visibility = fields.Boolean(string='State Visibility')
    state = fields.Selection(selection=[
        ('level1', 'Level 1'),
        ('level2', 'Level 2'),
        ('level3', 'Level 3'),
        ('level 4', 'Level 4'),
    ], string='Status', required=True, copy=False, tracking=True, default='level1')
    fields_level1 = fields.Char(string='Level', defaut="This is Level mess",
                                states={
                                    'level1': [('readonly', True), ('invisible', False), ('required', False)],
                                    'level2': [('invisible', True)],
                                    'level3': [('invisible', False)],
                                    'level 4': [('invisible', True)],
                                }
    )

    def test_copy(self):
        # single, create and return new record.
        result = self.copy({'age': self.age + 1})

    def test_default_get(self):
        """
            multiple, chỉ lấy giá trị mặc định của những trường trong class.
            nếu chỉ truyền list rỗng [] thì sẽ ko có kết quả.
            nếu trường truyền vào không có giá trị mặc định thì cũng ko có kết quả.
        """
        all = self.search([])
        result = all.default_get(['state_visibility', 'age'])
        print(f'result: {result}')

    def test_search(self):
        """
            @offset là loại bỏ số lượng kq trả về, nếu offset=3 mà tìm thấy 4 thì nó sẽ bỏ qua 3,
            cuối cùng kq trả về là 1.
            @limit
            @order = 'field_name'
            @count = Boolean: nếu có count. nó chỉ trả về số lượng kq thỏa mãn.
            :return recordset
            * Nếu có cả offset và limit thì offset sẽ được trừ trước, còn lại bao nhiêu thì mới tính limit
            (offset trừ bản ghi ở đầu recordset, limit trừ ở cuối)
        """
        result = self.search([('age', '<=', 18)], order='age')
        print('result', result)
        for r in result: print(r.name)

    def test_search_count(self):
        """
            @args: domain search
            search_count() giống với search() khi cho count=True vào.
            nếu muốn lấy kết quả là count thì nên dùng search_count()
            :return: int
        """
        result = self.search_count([('age', '<=', 18)])
        print(result)

    def test_name_search(self):
        """
            @name: key name để search với operator
            @operator: là toán tử để hình thành domain
            @args: tùy chọn domain thêm, khi đó nó sẽ kết hợp domain (args) và domain tự tạo trước đó (&)
            @limit
            :return: list tuple(id, text)
            ví dụ: [(2, <odoo.tools.func.lazy object at 0x89123>), (3, <odoo.tools.func.lazy object at 0x89123>)]
        """
        result = self.name_search(name='Student', operator='ilike', args=[('age', '=', 7)], limit=100)
        print(result)
        for r in result:
            id = r[0]
            record = self.browse(id)
            print(record.name)

    def test_read(self):
        """
            Khi cần lấy giá trị của record thì dùng read.
            @fields: 1 list các tên trường cần lấy giá trị, nếu để trống hoặc = None thì nó coi như là all field.
            :return: 1 list dict . 1 dict tương tứng với 1 bản ghi trong self.
                [{'field1', 'value1'}, {'field2', 'value2'}]
        """
        self = self.search([])
        result = self.read([])
        print(result)



    def test_read_group(self):
        """

        :return:
        """
        self = self.search([])
        result = self.read_group(domain=[], fields=[], groupby=['age'] )
        print(result)


    def gen30(self):
        for i in range(30):
            self.name_create(f'student {i}')

    def search2(self):
        all = self.search([])
        print(all)
        print('len all',len(all))
        s = self.search([], offset=10)
        print(s)
        print('len s', len(s))
        k =self.search([], limit=2, offset=1)
        print(len(k))
        print(k)
        # self.create()
        self.copy()
        # self.name_create()
        l = s.search([], limit=20)
        print(l)



    def test_cc(self):
        all_student = self.search([])
        # s = self.read(['name'])
        # print(self.mapped('name'))
        # print(s)
        s = self.fields_get()
        s1 = all_student.fields_get(['name'], ['readonly'])
        # print(s1)
        # s = self.fields_view_get(10)
        s1 = self.env['res.partner'].fields_view_get(view_type='tree')
        print(s1)
        # print(s1)
        # print(self._context)
        # self.unlink()

        # ir_ui_view = self.env.ref('schoolv3.form')
        # print(ir_ui_view)
        # self.exists()
        s = self.browse(19323)
        if not s.exists():
            print('not found!')
        print(s)
        print(s.exists())
        # self.ensure_one()
        # print(self.default_get([]))

        print(self.read())
        all_student = self.search([])
        list_tuple = all_student.name_get()  # [(id, name), ()...]
        print(list_tuple)
        metadatas = all_student.get_metadata()  #[{5 default filed + xmlid, noupdate}, {}...]
        print(metadatas)

        recordset1 = all_student.filtered(lambda r: len(r.name) > 1)
        # recordset2 = all_student.filtered('is_student2')
        s1 = all_student.filtered_domain([('name', '=', 'student 12')])
        # print(s1)

        r = self.mapped('name')  #['student 3']
        r_all = all_student.mapped('name')  #['student 1', 'Nguyen Van A', 'student 3',...]


        # print(r)
        # print(r_all)
        # print()
        # print(len(all_student), all_student)
        # print(self.search([], offset=10))
        # print(self.search([], limit=20))
        # print(self.search([], offset=10, limit=20))
        # print()
        print('\n\n\n')
        s1 = self.name_search('student')
        print(s1)
        s2 = self.name_search('student', args=[('state_visibility', '=', True)])
        print(s2)

        s3 = self.search(['&', ('name', 'ilike', 'student'), ('state_visibility', '=', True)], limit=100)
        print(s3)
        self.read()
        print('exists', all_student.exists())

        real_record = self.browse([9999,888, 16,17,18])

        print('ss', real_record.exists())
        print('\n\n\n\n')
        s = self.env.ref('base.user_admin')
        print(s)
        print(s.get_metadata())

    def oo(self):
        # r = self.name_create('dohaumenphai')
        # print(r)
        r = self.search([]).name_get()
        all_student = self.search([])
        print(r)
        self.write()
        self.flush()

        vals_list = [
            {'name': 'do', 'age': 10},
            {'name': 'men', 'age': 20}
        ]
        recordset = self.create(vals_list)

        print(recordset)

        new_record = self.create(vals_list=[{'name': 'do'}, {'name': 'do2'}])
        new_record = self.copy(default={'name': 'hau'})  # override giá trị copy

        print(new_record)

        default_value_dict = self.default_get(['name', 'age'])


        print(default_value_dict)

        list_tuple = self.name_create('name')  # return [(id, name)]

        print(list_tuple)

        always_True = all_student.write({'name': 'do'})  # update all student with name = 'do'

        print(always_True)

        self.flush(['name', 'age'], all_student)

        recordset = self.env['res.partner'].browse([1, 2, 3])  # res.partner(1, 2, 3)

        print(recordset)

        recordset = self.search(args=[], offset=1, limit=10, order='age', count=False)

        print(recordset)

        count = self.search_count(args=['name', '=', 'do'])

        print(count)

        recordset1 = self.name_search(name='do', args=None, operator='ilike', limit=100)
        recordset2 = self.name_search(name='do')

        print(recordset2)
        print(recordset1)

        result = all_student.read(['name'])  #[{'id': 1, 'name': 'ex1'}, ...]

        print(result)
        dict_field_attr = self.fields_get(['name'], ['readonly'])  #{'name': {'readonly': False}}
        #lấy thông tin thành phần chi tiết của view, {model, arch, name, type, ...}

        result_dict = self.fields_view_get(view_id=12, view_type='form', toolbar=False, submenu=False)

        print(result_dict)

        always_True = all_student.unlink()

        print(always_True)

        self.ensure_one()
        self.filtered()

    def test_domain(self):
        print(self.search([('name', 'like', 'Student')]))
        print(self.search([('name', 'ilike', 'StUDent')]))
        s = self.search([('name', 'not ilike', 'StUDent')])
        print(s)
        print(s.mapped('name'))
        print(self.search([('name', '=ilike', 'StuDent%')]))
        print(self.search([('name', '=like', 'StuDent%')]))

        print(self.search([('name', 'in', ['Student 1', 'Student 2'])]))
        print(self.search([('name', 'in', ('Student 1', 'Student 2'))]))

class Tes1t1(models.Model):
    _name = 'test1.test1'

    age = fields.Integer()

    def test(self):
        print(self.name_get())

