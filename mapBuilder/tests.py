from django.test import TestCase

from mapBuilder.room_generator import generateRoom
from mapBuilder.models import Room
from mapBuilder.services import RoomAdjacencyService


class RoomAdjacencyServiceTestCase(TestCase):
    def test_initial_room_generation(self):
        self.assertEqual(Room.objects.count(), 0)
        room1 = generateRoom()
        self.assertEqual(Room.objects.count(), 1)
        room2 = generateRoom()
        self.assertEqual(Room.objects.count(), 2)
        self.assertEqual(room1.exits.all()[0], room2)

        rooms = [room1, room2]
        for idx in range(20):
            new_room = generateRoom()
            self.assertNotEqual(new_room.exits.count(), 0)

        for room in Room.objects.all():
            self.assertLessEqual(room.exits.count(), 4)

    def test_adjacency_reroll(self):
        [generateRoom() for i in range(20)]
        RoomAdjacencyService().reorganize_rooms()

