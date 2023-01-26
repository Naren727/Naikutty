from django import forms


class Userforms(forms.Form):
    name = forms.CharField(max_length=25)
    gfc = forms.ChoiceField(choices=[("2-3 Times a Week Brushing", "2-3 Times a Week Brushing"),
                                     ("Daily Brushing", "Daily Brushing"),
                                     ("Occasional Bath/Brush", "Occasional Bath/Brush"),
                                     ("Specialty/Professional", "Specialty/Professional"),
                                     ("Weekly Brushing", "Weekly Brushing")])
    sc = forms.ChoiceField(choices=[("Frequent", "Frequent",),
                                    ("Infrequent", "Infrequent",),
                                    ("Occasional", "Occasional"),
                                    ("Regularly", "Regularly"),
                                    ("Seasonal", "Seasonal")])
    elc = forms.ChoiceField(choices=[("Calm", "Calm"),
                                     ("Couch Potato", "Couch Potato"),
                                     ("Energetic", "Energetic"),
                                     ("Needs Lots of Activity", "Needs Lots of Activity"),
                                     ("Regular Exercise", "Regular Exercise")])
    tc = forms.ChoiceField(choices=[("Agreeable", "Agreeable"),
                                    ("Eager to Please", "Eager to Please"),
                                    ("Easy Training", "Easy Training"),
                                    ("Independent", "Independent"),
                                    ("May be Stubborn", "May be Stubborn")])
    dc = forms.ChoiceField(choices=[("Alert/Responsive", "Alert/Responsive"),
                                    (" Aloof/Wary", " Aloof/Wary"),
                                    ("Friendly", "Friendly"),
                                    ("Outgoing", "Outgoing"),
                                    ("Reserved with Strangers", "Reserved with Strangers")])
