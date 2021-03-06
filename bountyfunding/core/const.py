from bountyfunding.util.enum import Enum

class ProjectType(Enum):
    NORMAL = 10
    TEST = 20
    ROOT = 30
    GITHUB = 40

class IssueStatus(Enum):
    READY = 10
    STARTED = 20
    COMPLETED = 30

class SponsorshipStatus(Enum):
    PLEDGED = 10
    CONFIRMED = 20
    VALIDATED = 30
    TRANSFERRED = 40
    REJECTED = 50
    REFUNDED = 60

class PaymentStatus(Enum):
    INITIATED = 10
    CONFIRMED = 20

class PaymentGateway(Enum):
    DUMMY = 10
    PAYPAL_STANDARD = 21
    PAYPAL_ADAPTIVE = 22


