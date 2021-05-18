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
