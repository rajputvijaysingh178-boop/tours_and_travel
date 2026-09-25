class HotelAllocationService:

    hotels = []
    rooms = {}
    allocations = {}

    def create_hotel(self, hotel):
        hotel_id = len(self.hotels) + 1

        data = {
            "hotel_id": hotel_id,
            "name": hotel.name,
            "location": hotel.location
        }

        self.hotels.append(data)
        self.rooms[hotel_id] = []

        return data

    def get_hotels(self):
        return self.hotels

    def add_room(self, hotel_id, room):
        if hotel_id not in self.rooms:
            return None

        room_data = {
            "room_id": len(self.rooms[hotel_id]) + 1,
            "room_number": room.room_number,
            "room_type": room.room_type,
            "price": room.price,
            "available": room.available
        }

        self.rooms[hotel_id].append(room_data)

        return room_data

    def get_availability(self, hotel_id):
        if hotel_id not in self.rooms:
            return None

        return [
            room for room in self.rooms[hotel_id]
            if room["available"]
        ]

    def allocate_room(self, booking_id, hotel_id, room_id):
        if hotel_id not in self.rooms:
            return None

        for room in self.rooms[hotel_id]:
            if room["room_id"] == room_id and room["available"]:

                room["available"] = False

                allocation = {
                    "booking_id": booking_id,
                    "hotel_id": hotel_id,
                    "room_id": room_id,
                    "status": "allocated"
                }

                self.allocations[booking_id] = allocation

                return allocation

        return None