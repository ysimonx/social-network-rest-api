from ..model_dir.people import People
from ..model_dir.gallery import Gallery, Picture, Video
from ..model_dir.meeting import Meeting, Country, City, Address, Tour

class Api():
    def xget_people_full(self, people_id):
        people = People.query.get(people_id)

        result = people.to_json()
        
        result_galleries = []
            
        galleries = Gallery.query.filter(Gallery.people_id == people.id)
        for gallery in galleries:
            upgraded_gallery = gallery.to_json()
            pictures = Picture.query.filter(Picture.gallery_id == gallery.id)
            if pictures is None:
                upgraded_gallery['pictures'] = []
            else:
                upgraded_gallery['pictures'] = [picture.to_json() for picture in pictures]
            videos = Video.query.filter(Video.gallery_id == gallery.id)
            if videos is None:
                upgraded_gallery['videos'] = []
            else:
                upgraded_gallery['videos'] = [video.to_json() for video in videos]

            result_galleries.append(upgraded_gallery)

        result_tours = []
        tours = Tour.query.filter(Tour.people_id == people.id)
        for tour in tours:
            upgraded_tour = tour.to_json()
            result_tours.append(upgraded_tour)

        result['galleries'] = [result_gallery for result_gallery in result_galleries]
        result['tours'] = [result_tour for result_tour in result_tours]

        return result

