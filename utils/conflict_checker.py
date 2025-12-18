from models import db, Event, EventResourceAllocation

def is_resource_available(resource_id, start_time, end_time, exclude_event_id=None):
    """
    Checks if a resource is available for the given time range.
    
    Args:
        resource_id: The ID of the resource to check.
        start_time: start datetime of the new event.
        end_time: end datetime of the new event.
        exclude_event_id: Optional ID of an event to exclude from the check (used during edit).
        
    Returns:
        tuple: (available: bool, conflict_reason: str or None)
    """
    
    # Query for allocations involving this resource
    query = db.session.query(Event).join(EventResourceAllocation).filter(
        EventResourceAllocation.resource_id == resource_id
    )
    
    if exclude_event_id:
        query = query.filter(Event.id != exclude_event_id)
        
    # Overlap logic: (StartA < EndB) and (EndA > StartB)
    # We want to find any event where NOT (EndExisting <= StartNew OR StartExisting >= EndNew)
    # But checking for overlap directly is often easier.
    # An overlap exists if:
    # Existing.start < New.end AND Existing.end > New.start
    
    conflicting_events = query.filter(
        Event.start_time < end_time,
        Event.end_time > start_time
    ).all()
    
    if conflicting_events:
        event = conflicting_events[0]
        return False, f"Conflict with event '{event.title}' ({event.start_time} - {event.end_time})"
        
    return True, None
