from modeltranslation.translator import TranslationOptions
from modeltranslation.translator import translator

from .models import Product , Category , SubCategory

class ProductTranslationOptions(TranslationOptions):
    fields = ("name", "description")
    
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name",)
    
class SubCategoryTranslationOptions(TranslationOptions):
    fields = ("name",)
    


translator.register(SubCategory, SubCategoryTranslationOptions)
translator.register(Category, CategoryTranslationOptions)
translator.register(Product, ProductTranslationOptions)