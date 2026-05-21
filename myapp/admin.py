from django.contrib import admin
from .models import ScrapPrice, QuoteRequest, PickupBooking, ContactMessage, Comment
from django.utils.html import format_html


from .models import PageView
from django.utils.timezone import now
from datetime import timedelta

# ── Scrap Prices ──────────────────────────────────────────
@admin.register(ScrapPrice)
class ScrapPriceAdmin(admin.ModelAdmin):
    list_display  = ('material', 'scrap_type', 'price_per_kg', 'unit', 'updated_at')
    list_editable = ('price_per_kg',)          # edit price directly in the list!
    list_filter   = ('scrap_type',)
    search_fields = ('material',)
    ordering      = ('scrap_type',)

# ── Quote Requests ────────────────────────────────────────
@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display  = ('name', 'phone', 'scrap_type', 'weight_kg', 'estimated_price', 'created_at')
    list_filter   = ('scrap_type',)
    search_fields = ('name', 'phone')
    readonly_fields = ('created_at',)
    ordering      = ('-created_at',)

# ── Pickup Bookings ───────────────────────────────────────
@admin.register(PickupBooking)
class PickupBookingAdmin(admin.ModelAdmin):
    list_display  = ('name', 'phone', 'scrap_type', 'pickup_date', 'status', 'created_at')
    list_editable = ('status',)                # change status directly in list!
    list_filter   = ('status', 'scrap_type', 'pickup_date')
    search_fields = ('name', 'phone', 'address')
    readonly_fields = ('created_at',)
    ordering      = ('-pickup_date',)

    # color-coded status in list (optional visual upgrade)
    def status_display(self, obj):
        colors = {'pending': 'orange', 'confirmed': 'blue', 'done': 'green'}
        color  = colors.get(obj.status, 'black')
        return format_html('<b style="color:{}">{}</b>', color, obj.get_status_display())
    status_display.short_description = 'Status'

# ── Contact Messages ──────────────────────────────────────
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ('name', 'phone', 'created_at', 'short_message')
    search_fields = ('name', 'phone')
    readonly_fields = ('name', 'phone', 'message', 'created_at')  # read-only inbox
    ordering      = ('-created_at',)

    def short_message(self, obj):
        return obj.message[:60] + '...' if len(obj.message) > 60 else obj.message
    short_message.short_description = 'Message'

# ── Comments ──────────────────────────────────────────────
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display  = ('user', 'short_content', 'created_at')
    search_fields = ('user__username', 'content')
    readonly_fields = ('user', 'created_at')
    ordering      = ('-created_at',)

    def short_content(self, obj):
        return obj.content[:60] + '...' if len(obj.content) > 60 else obj.content
    short_content.short_description = 'Comment'


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('path', 'ip_address', 'visited_at')
    list_filter  = ('path',)
    ordering     = ('-visited_at',)
    readonly_fields = ('path', 'ip_address', 'visited_at')

    # show summary stats at top of changelist
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        today     = now().date()
        week_ago  = today - timedelta(days=7)

        extra_context['today_views'] = PageView.objects.filter(visited_at__date=today).count()
        extra_context['week_views']  = PageView.objects.filter(visited_at__date__gte=week_ago).count()
        extra_context['total_views'] = PageView.objects.count()

        return super().changelist_view(request, extra_context=extra_context)