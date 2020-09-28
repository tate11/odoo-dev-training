from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BookCategory(models.Model):
    _name = 'library.book.category'
    _description = 'Library Book Category'
    _parent_store = True
    #_parent_name = 'parent_id'

    name = fields.Char('Category')
    description = fields.Text('Description')
    parent_id = fields.Many2one('library.book.category', string='Parent Category', ondelete='restrict', index=True)
    child_ids = fields.One2many('library.book.category', 'parent_id', string='Child Categories')
    parent_path = fields.Char(index=True)

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError('Error! You cannot create recursive categories.')

    def create_dummy_categories(self):
        cat1 = {
            'name': 'Python',
            'description': 'Books about python programming'
        }
        cat2 = {
            'name': 'Java',
            'description': 'Books about java programming'
        }
        parent_cat = {
            'name': 'Programming',
            'description': 'Books about programming languages',
            'child_ids': [(0, 0, cat1), (0, 0, cat2)]
        }
        record = self.env['library.book.category'].create(parent_cat)