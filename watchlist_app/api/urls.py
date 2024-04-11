from django.urls import path, include
from rest_framework.routers import DefaultRouter

# from watchlist_app.api.views import movie_list, movie_details
from watchlist_app.api.views import (
    WatchListAV,
    WatchDetailAV,
    StreamPlatformAV,
    StreamDetailAV,
    ReviewList,
    ReviewDetail,
    ReviewCreate,
    StreamPlatformVS,
    UserReview,
    WatchListGV
)

router = DefaultRouter()
router.register("stream", StreamPlatformVS, basename="streamplatformvs")

urlpatterns = [
    path("list/", WatchListAV.as_view(), name="movie-list-api-view-class"),
    path("<int:pk>/", WatchDetailAV.as_view(), name="movie-details"),
    path("list2/", WatchListGV.as_view(), name="movie-list-with-generic-view-class"),
    # path('stream/',StreamPlatformAV.as_view(), name="stream-list"),
    # path('stream/<int:pk>', StreamDetailAV.as_view(),name='stream-details'),
    path("", include(router.urls)),
    # path('review/',ReviewList.as_view(),name='review-list'),
    # path('review/<int:pk>',ReviewDetail.as_view(),name='review-detail')
    path("<int:pk>/reviews/", ReviewList.as_view(), name="review-list"),               #Here id is watchlist id
    path("<int:pk>/review-create/", ReviewCreate.as_view(), name="review-create"),
    path("review/<int:pk>/", ReviewDetail.as_view(), name="review-detail"),            #Enter review_id in int:pk
    path("reviews/", UserReview.as_view(), name="user-review-detail"),
]
