from django.core.management.base import BaseCommand
from pharma.models import Medicine

class Command(BaseCommand):
    help = 'Updates medicines with generic names, categories and prescription requirements'

    def handle(self, *args, **kwargs):
        # Dictionary mapping medicine names to their generic names, categories and prescription requirements
        medicine_data = {
            'Paracetamol': {
                'generic_name': 'Acetaminophen',
                'category': 'Pain Relief',
                'prescription_required': False
            },
            'Amoxicillin': {
                'generic_name': 'Amoxicillin',
                'category': 'Antibiotics',
                'prescription_required': True
            },
            'Omeprazole': {
                'generic_name': 'Omeprazole',
                'category': 'Gastrointestinal',
                'prescription_required': True
            },
            'Metformin': {
                'generic_name': 'Metformin Hydrochloride',
                'category': 'Diabetes',
                'prescription_required': True
            },
            'Amlodipine': {
                'generic_name': 'Amlodipine Besylate',
                'category': 'Cardiovascular',
                'prescription_required': True
            },
            'Cetirizine': {
                'generic_name': 'Cetirizine Hydrochloride',
                'category': 'Antihistamine',
                'prescription_required': False
            },
            'Aspirin': {
                'generic_name': 'Acetylsalicylic Acid',
                'category': 'Pain Relief',
                'prescription_required': False
            },
            'Vitamin D3': {
                'generic_name': 'Cholecalciferol',
                'category': 'Supplements',
                'prescription_required': False
            }
        }

        updated_count = 0
        for medicine in Medicine.objects.all():
            if medicine.name in medicine_data:
                data = medicine_data[medicine.name]
                medicine.generic_name = data['generic_name']
                medicine.category = data['category']
                medicine.prescription_required = data['prescription_required']
                medicine.save()
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Updated {medicine.name} with generic name "{data["generic_name"]}", '
                        f'category "{data["category"]}", '
                        f'prescription required: {data["prescription_required"]}'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully updated {updated_count} medicines'
            )
        ) 