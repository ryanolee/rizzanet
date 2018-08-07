''' The events module for rizzanet. This module uses a Pub-Sub model for binding and dispaching events inturnaly '''
from .eventpool import GlobalEventPool, getEventPool, attachEventListener, dispatchEvent
from .on import on
