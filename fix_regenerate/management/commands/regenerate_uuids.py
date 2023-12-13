import uuid
import math
import time
import os
from django.core.management.base import BaseCommand
from fix_regenerate.models import Ticket

class Command(BaseCommand):
    help = 'Regenerate UUID values for Ticket records'

    def add_arguments(self, parser):
        parser.add_argument('--chunk-size', type=int, default=10000, help='Number of records to process in each iteration')

    def handle(self, *args, **options):
        chunk_size = options['chunk_size']
        progress_file = 'uuid_regeneration_progress.txt'

        total_records = Ticket.objects.count()
        total_chunks = math.ceil(total_records / chunk_size)

        start_time = time.time()
        processed_records = 0

        # Check for progress file and resume from the last processed record
        if os.path.exists(progress_file):
            with open(progress_file, 'r') as f:
                last_processed_record_id = int(f.read())
                start_chunk = last_processed_record_id // chunk_size
        else:
            last_processed_record_id = 0
            start_chunk = 0

        self.stdout.write(self.style.SUCCESS(f'Starting UUID regeneration for {total_records} records...'))

        try:
            for chunk_number in range(start_chunk, total_chunks):
                offset = chunk_number * chunk_size
                tickets = Ticket.objects.order_by('id').only('id', 'token').values_list('id', 'token')[offset:offset + chunk_size]

                for ticket_id, old_token in tickets:
                    if ticket_id <= last_processed_record_id:
                        continue  # Skip records that were already processed

                    new_token = uuid.uuid4()
                    Ticket.objects.filter(id=ticket_id, token=old_token).update(token=new_token)
                    processed_records += 1

                    if processed_records % 100 == 0:
                        elapsed_time = time.time() - start_time
                        records_per_second = processed_records / elapsed_time
                        remaining_records = total_records - processed_records
                        estimated_time_remaining = remaining_records / records_per_second

                        self.stdout.write(self.style.SUCCESS(
                            f'Processed {processed_records}/{total_records} records. '
                            f'Estimated time remaining: {estimated_time_remaining:.2f} seconds.'
                        ))

        except KeyboardInterrupt:
            # Save progress to file
            with open(progress_file, 'w') as f:
                f.write(str(ticket_id))
            self.stdout.write(self.style.WARNING('Script interrupted. Saving progress...'))
        else:
            self.stdout.write(self.style.SUCCESS('UUID regeneration completed successfully. Removing progress file.'))
            os.remove(progress_file)

        elapsed_time = time.time() - start_time
        self.stdout.write(self.style.SUCCESS(f'Total time: {elapsed_time:.2f} seconds.'))

