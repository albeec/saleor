import json

from django import forms
from django.utils.encoding import smart_text
from django.utils.translation import pgettext_lazy
from django_prices.templatetags.prices import amount
from draftjs_sanitizer import SafeJSONEncoder

from ..checkout.forms import AddToCheckoutForm
from ..wishlist.forms import AddToWishlistForm
from ..core.taxes import display_gross_prices


class VariantChoiceField(forms.ModelChoiceField):
    discounts = None
    country = None
    display_gross = True
    taxes = None
    extensions = None

    def label_from_instance(self, obj):
        variant_label = smart_text(obj)
        price = self.extensions.apply_taxes_to_product(
            obj.product, obj.get_price(self.discounts), self.country
        )
        price = price.gross if self.display_gross else price.net
        label = pgettext_lazy(
            "Variant choice field label", "%(variant_label)s - %(price)s"
        ) % {"variant_label": variant_label, "price": amount(price)}
        return label

    def update_field_data(self, variants, discounts, country, extensions=None):
        """Initialize variant picker metadata."""
        self.queryset = variants
        self.discounts = discounts
        self.country = country
        self.extensions = extensions
        self.empty_label = None
        self.display_gross = display_gross_prices()
        images_map = {
            variant.pk: [vi.image.image.url for vi in variant.variant_images.all()]
            for variant in variants.all()
        }
        self.widget.attrs["data-images"] = json.dumps(images_map, cls=SafeJSONEncoder)
        # Don't display select input if there is only one variant.
        if self.queryset.count() == 1:
            self.widget = forms.HiddenInput({"value": variants.all()[0].pk})


class ProductForm(AddToCheckoutForm):
    variant = VariantChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        variant_field = self.fields["variant"]
        shipping_address = self.checkout.shipping_address
        country = shipping_address.country if shipping_address else self.country
        variant_field.update_field_data(
            self.product.variants.all(), self.discounts, country, self.extensions
        )

    def get_variant(self, cleaned_data):
        return cleaned_data.get("variant")


class WishlistForm(AddToWishlistForm):
    variant = VariantChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        variant_field = self.fields["variant"]
        shipping_address = self.wishlist.shipping_address
        country = shipping_address.country if shipping_address else self.country
        variant_field.update_field_data(
            self.product.variants.all(), self.discounts, country, self.extensions
        )

    def get_variant(self, cleaned_data):
        return cleaned_data.get("variant")
