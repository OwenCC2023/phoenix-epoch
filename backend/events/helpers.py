"""Helper to apply event effects to nations."""
from nations.models import NationModifier


def apply_event_to_nations(event, nations):
    """Apply event effects (modifiers, population changes) to the given nations."""
    effects = event.effects
    modifiers = effects.get("modifiers", [])
    pop_change = effects.get("population_change", 0)

    for nation in nations:
        # Apply modifiers
        for mod_def in modifiers:
            duration = mod_def.get("duration")
            expires = event.turn_number + duration if duration else None
            NationModifier.objects.create(
                nation=nation,
                name=f"Event: {event.title} - {mod_def['target']}",
                category=mod_def["category"],
                target=mod_def["target"],
                modifier_type=mod_def["modifier_type"],
                value=mod_def["value"],
                source=NationModifier.Source.EVENT,
                expires_turn=expires,
            )

        # Apply population changes
        if pop_change:
            provinces = nation.provinces.all()
            if provinces:
                # Distribute evenly
                per_province = pop_change // provinces.count()
                for province in provinces:
                    province.population = max(100, province.population + per_province)
                    province.save(update_fields=["population"])
