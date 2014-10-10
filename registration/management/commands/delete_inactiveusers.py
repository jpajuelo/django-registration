"""
    Copyright (c) 2014, Jaime Pajuelo.
    All rights reserved.

    Code released under the BSD 2-Clause license.
"""

from django.core.management.base import make_option, NoArgsCommand
from registration.models import ActivationCode


class Command(NoArgsCommand):

    help = "Remove users associated with an activation code expired."
    option_list = NoArgsCommand.option_list + (
        make_option(
            '--noinput', action='store_false', default=True,
            dest='interactive',
            help="Do NOT prompt the user for input of any kind."
        ),
    )

    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity', 1))
        removed = 0

        self.stdout.write(
            "\nThe following operation IRREPARABLY will remove inactive users"
            " which are associated with an activation code expired from the"
            " database.\nNOTE: if an active user is associated with an"
            " activation code, in this case this activation code will ONLY"
            " be removed.\n")

        prompt = "\nAre you sure you wish to continue? [y/N] "

        if options['interactive'] and raw_input(prompt) not in ["y", "yes"]:
            self.stderr.write("\nOperation has been canceled.")
            return

        if verbosity > 1:
            self.stdout.write("\nRemoving from the database...")

        for i in ActivationCode.objects.all():
            if i.user.is_active:
                i.delete()
            elif i.is_expired():
                i.user.delete()
                removed += 1
                if verbosity > 1:
                    self.stdout.write("The user '%s' was deleted." % i.user)

        self.stdout.write("\n%s users were removed successfully." % removed)
