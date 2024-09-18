from datetime import date, timedelta
from django import template

register = template.Library()


@register.filter
def get_menu_for_day(day, daily_menus):
    return daily_menus.filter(served_at=day).first()


@register.filter
def get_card_class(day):
    day = day.date()
    today = date.today()
    tomorrow = today + timedelta(days=1)

    if day < today:
        return "past-card-header"
    elif day == today:
        return "today-card-header"
    elif day == tomorrow:
        return "tomorrow-card-header"
    else:
        return "future-card-header"


@register.filter
def is_weekend(day):
    return day.weekday in [5,6]


@register.filter
def category_in_menu_items(menu, category):
    menu_categories = menu.menu_items.values_list('category__name', flat=True)
    return category.name in menu_categories


@register.filter
def get_menu_item_with_category(menu_items, category):
    return menu_items.filter(category=category)
