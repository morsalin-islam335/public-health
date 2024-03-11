from django.urls import path 


from . views import addVaccine, AddScheduleView, editSchedule, deleteSchedule,  BookDose, vacDetails, addSchedule


urlpatterns = [
    path("addVaccine", addVaccine, name = 'addVaccine'),
    path("addSchedule", addSchedule, name = 'addSchedule'),
    # path("addSchedule", AddScheduleView.as_view(), name = 'addSchedule'),
    path("editSchedule/<int:id>", editSchedule, name = 'editSchedule'),
    path("deleteSchedule/<int:id>", deleteSchedule, name = 'deleteSchedule'),
    path("patient/bookDose/", BookDose.as_view(), name = 'bookDose'),
    path("vaccineDetails/<int:id>/",vacDetails, name =  'vacDetails')
    
    # path("patient/giveReview/", giveReview, name = 'giveReview'),
]
