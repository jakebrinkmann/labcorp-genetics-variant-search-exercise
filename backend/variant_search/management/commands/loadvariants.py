import csv
import gzip
from typing import TYPE_CHECKING

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils.dateparse import parse_datetime

from variant_search.models import Variant

if TYPE_CHECKING:
    from argparse import ArgumentParser


def is_variant_data_loaded(force_load: bool) -> bool:
    if Variant.objects.exists():
        if force_load:
            print(f"Deleting existing variants in database.")
            Variant.objects.all().delete()
        else:
            return True
    return False


class Command(BaseCommand):
    help = "Generate fixture dataset"

    def add_arguments(self, parser: "ArgumentParser"):
        parser.add_argument(
            "--force",
            action="store_true",
            help="delete existing variants and then load variant data",
        )
        parser.add_argument(
            "--load-all",
            action="store_true",
            help="load the larger variants_all.tsv.gz file",
        )

    def handle(self, *args, **options):
        expected_columns = 23

        if is_variant_data_loaded(options["force"]):
            print("Skipping loadvariants command. Variants already loaded in database.")
            return

        if options["load_all"]:
            filehandle = gzip.open("../data/variants_all.tsv.gz", "rt")
        else:
            filehandle = open("../data/variants.tsv", "rt")

        csv_file = csv.reader(filehandle, delimiter="\t")

        line_number = 0
        current_batch = []
        for variant_data in csv_file:
            # Skip the header
            if line_number == 0:
                line_number = line_number + 1
                continue

            # some lines don't have all the columns - in that case, add empty strings
            data_length = len(variant_data)
            if data_length < expected_columns:
                for _ in range(expected_columns - data_length):
                    variant_data.append("")

            variant = Variant(
                gene=variant_data[0],
                nucleotide_change=variant_data[1],
                protein_change=variant_data[2],
                other_mappings=variant_data[3],
                alias=variant_data[4],
                transcripts=variant_data[5],
                region=variant_data[6],
                reported_classification=variant_data[7],
                inferred_classification=variant_data[8],
                source=variant_data[9],
                last_evaluated=parse_datetime(variant_data[10] + " UTC")
                if len(variant_data[10])
                else None,
                last_updated=parse_datetime(variant_data[11] + " UTC")
                if len(variant_data[11])
                else None,
                url=variant_data[12],
                submitter_comment=variant_data[13],
                assembly=variant_data[14],
                chr=variant_data[15],
                genomic_start=variant_data[16],
                genomic_stop=variant_data[17],
                ref=variant_data[18],
                alt=variant_data[19],
                accession=variant_data[20],
                reported_ref=variant_data[21],
                reported_alt=variant_data[22],
            )
            current_batch.append(variant)

            if (line_number + 1) % 1000 == 0:
                print(f"Loaded {line_number+1} variants")
                if current_batch:
                    try:
                        # TODO: is 'create' enough, or we expect updates?
                        Variant.objects.bulk_create(current_batch)
                    except IntegrityError as exc:
                        # TODO: can we recover from this?
                        print(exc)
                    except Exception as exc:
                        print(exc)
                    finally:
                        current_batch = []

            line_number = line_number + 1

        print(f"Success! Saved {line_number} variants")
