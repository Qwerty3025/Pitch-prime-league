from league.models import Team
from .models import PartnerLogo


def footer_context(request):
    teams = Team.objects.select_related('season').filter(logo__isnull=False).exclude(logo='').order_by('name')
    sponsors = PartnerLogo.objects.filter(is_active=True, category='sponsor').order_by('sort_order', 'name')
    suppliers = PartnerLogo.objects.filter(is_active=True, category='supplier').order_by('sort_order', 'name')

    return {
        'footer_teams': teams,
        'footer_sponsors': sponsors,
        'footer_suppliers': suppliers,
    }
