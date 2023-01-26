from django.db import models


# Models for the Main Form

class Main_Model(models.Model):
    gfc_CHOICES = (("2-3 Times a Week Brushing", "2-3 Times a Week Brushing"),
                   ("Daily Brushing", "Daily Brushing"),
                   ("Occasional Bath/Brush", "Occasional Bath/Brush"),
                   ("Specialty/Professional", "Specialty/Professional"),
                   ("Weekly Brushing", "Weekly Brushing")
                   )
    sc_CHOICES = (("Frequent", "Frequent",),
                  ("Infrequent", "Infrequent",),
                  ("Occasional", "Occasional"),
                  ("Regularly", "Regularly"),
                  ("Seasonal", "Seasonal")
                  )
    elc_CHOICES = (("Calm", "Calm"),
                   ("Couch Potato", "Couch Potato"),
                   ("Energetic", "Energetic"),
                   ("Needs Lots of Activity", "Needs Lots of Activity"),
                   ("Regular Exercise", "Regular Exercise"))
    tc_CHOICES = (("Agreeable", "Agreeable"),
                  ("Eager to Please", "Eager to Please"),
                  ("Easy Training", "Easy Training"),
                  ("Independent", "Independent"),
                  ("May be Stubborn", "May be Stubborn"))
    dc_CHOICES = (("Alert/Responsive", "Alert/Responsive"),
                  (" Aloof/Wary", " Aloof/Wary"),
                  ("Friendly", "Friendly"),
                  ("Outgoing", "Outgoing"),
                  ("Reserved with Strangers", "Reserved with Strangers"))

    name = models.CharField(max_length=25)
    gfc = models.CharField(max_length=30, choices=gfc_CHOICES)
    sc = models.CharField(max_length=30, choices=sc_CHOICES)
    elc = models.CharField(max_length=30, choices=elc_CHOICES)
    tc = models.CharField(max_length=30, choices=tc_CHOICES)
    dc = models.CharField(max_length=30, choices=dc_CHOICES)

    def __str__(self):
        return self.name
