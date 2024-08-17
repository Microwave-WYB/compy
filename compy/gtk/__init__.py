from compy.gtk.widget import (
    GtkBoxWidget,
    GtkButtonWidget,
    GtkColumnWidget,
    GtkRowWidget,
    GtkTextWidget,
)
from compy.widget import BoxWidget, ButtonWidget, ColumnWidget, RowWidget, TextWidget, Widget

GTK_IMPLEMENTATIONS: dict[type[Widget], type[Widget]] = {
    TextWidget: GtkTextWidget,
    ButtonWidget: GtkButtonWidget,
    BoxWidget: GtkBoxWidget,
    RowWidget: GtkRowWidget,
    ColumnWidget: GtkColumnWidget,
}
