import os
import sys
from datetime import datetime
from dotenv import load_dotenv
import requests
from tabulate import tabulate


def display_welcome():
    """Display a welcome message for the application"""
    print("=" * 60)
    print("          IRCTC TRAIN MANAGEMENT SYSTEM")
    print("=" * 60)
    print("\nWelcome to the IRCTC Train Information Portal!")


class IRCTC:
    def __init__(self):
        """Initialize the IRCTC Train Management System"""
        # API key should be kept safe in production code
        load_dotenv()
        self.API_KEY = os.getenv("ENV_API_KEY")
        self.BASE_URL = os.getenv("BASE_URL")
        display_welcome()
        self.main_menu()

    def main_menu(self):
        """Display the main menu and handle user selection"""
        while True:
            print("\n" + "=" * 60)
            user = input("""How would you proceed?
        1. Enter 1 to Check Trains From Your Station
        2. Enter 2 to Check PNR Status
        3. Enter 3 to Check Station Schedule of a Train
        4. Enter 4 to Search Trains Between Stations
        5. Enter 5 to Check Train Fare
        6. Enter 6 to Check Seat Availability
        0. Enter 0 to Exit\n""")

            try:
                if user == "1":
                    station_code = input("Enter the Station Code (e.g., NDLS for New Delhi): ").upper()
                    self.train_search(station_code)
                elif user == "2":
                    pnr_no = input("Enter the 10-digit PNR Number: ")
                    self.pnr_check(pnr_no)
                elif user == "3":
                    train_no = input("Enter the Train Number: ")
                    self.train_dtl(train_no)
                elif user == "4":
                    src = input("Enter Source Station Code: ").upper()
                    dst = input("Enter Destination Station Code: ").upper()
                    date = input("Enter Date (DD-MM-YYYY): ")
                    self.search_trains_between_stations(src, dst, date)
                elif user == "5":
                    self.check_train_fare()
                elif user == "6":
                    self.check_seat_availability()
                elif user == "0":
                    print("Thank you for using IRCTC Train Management System!")
                    break
                else:
                    print("Invalid option! Please try again.")
            except Exception as e:
                print(f"An error occurred in menu selection: {str(e)}")
                print("Please try again.")

    def train_search(self, station_code):
        """Fetch and display all trains passing through a particular station"""
        print(f"\nFetching trains for station code: {station_code}...")
        try:
            # Make API request to get trains on station
            url = f"{self.BASE_URL}/AllTrainOnStation/apikey/{self.API_KEY}/StationCode/{station_code}"
            response = requests.get(url)
            data = response.json()

            # Check if the response is a success
            if str(data.get("ResponseCode")) == "200":
                # Extract train data
                trains = data.get("Trains", [])
                if trains:
                    # Prepare data for tabulating
                    table_data = []
                    for train in trains:
                        table_data.append([
                            train.get("TrainNo", "N/A"),
                            train.get("TrainName", "N/A").strip(),
                            train.get("ArrivalTime", "N/A"),
                            train.get("DepartureTime", "N/A"),
                            f"{train.get('Source', '???')} ➔ {train.get('Destination', '???')}"
                        ])

                    # Display data in tabular format
                    headers = ["Train No.", "Train Name", "Arrival", "Departure", "Route"]
                    print("\nTrains at station:", data.get("StationName", station_code))
                    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
                else:
                    print(f"No trains found for station code {station_code}")
            else:
                print(f"Error: {data.get('Message', 'Unknown error')}")
        except requests.exceptions.RequestException as re:
            print(f"Network error: {str(re)}")
            print("Please check your internet connection and try again.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def pnr_check(self, pnr_no):
        """Check PNR status for a given PNR number"""
        print(f"\nChecking PNR status for: {pnr_no}...")
        try:
            # Validate PNR number
            if not (pnr_no.isdigit() and len(pnr_no) == 10):
                print("Invalid PNR format. PNR should be a 10-digit number.")
                return

            # Make API request for PNR status
            url = f"{self.BASE_URL}/PNRCheck/apikey/{self.API_KEY}/PNRNumber/{pnr_no}"
            response = requests.get(url)
            data = response.json()

            # Check if the response is a success
            if str(data.get("ResponseCode")) == "200":
                # Display PNR details
                print("\n" + "=" * 60)
                print(f"PNR Number: {data.get('Pnr', 'N/A')}")
                print(f"Train Number: {data.get('TrainNo', 'N/A')}")
                print(f"Train Name: {data.get('TrainName', 'N/A')}")
                print(f"DOJ: {data.get('Doj', 'N/A')}")
                print(f"From: {data.get('From', 'N/A')}")
                print(f"To: {data.get('To', 'N/A')}")
                print(f"Class: {data.get('Class', 'N/A')}")

                # Display passenger details
                if "PassengerStatus" in data:
                    print("\nPassenger Details:")
                    headers = ["No.", "Booking Status", "Current Status"]
                    passengers = []
                    for i, passenger in enumerate(data["PassengerStatus"], 1):
                        passengers.append([
                            i,
                            passenger.get("BookingStatus", "N/A"),
                            passenger.get("CurrentStatus", "N/A")
                        ])
                    print(tabulate(passengers, headers=headers, tablefmt="simple"))

                print("\n" + data.get("ChartPrepared", "Chart not prepared"))
            else:
                print(f"Error: {data.get('Message', 'Unknown error')}")
        except requests.exceptions.RequestException as re:
            print(f"Network error: {str(re)}")
            print("Please check your internet connection and try again.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def train_dtl(self, train_no):
        """Fetch and display the schedule of a train"""
        print(f"\nFetching schedule for train number: {train_no}...")
        try:
            # Make API request for train schedule
            url = f"{self.BASE_URL}/TrainSchedule/apikey/{self.API_KEY}/TrainNumber/{train_no}"
            response = requests.get(url)
            data = response.json()

            # Check if the response is a success
            if str(data.get("ResponseCode")) == "200":
                # Display train information
                print("\n" + "=" * 60)
                print(f"Train Number: {data.get('TrainNumber', 'N/A')}")
                print(f"Train Name: {data.get('TrainName', 'N/A')}")
                print(f"From: {data.get('Source', 'N/A')}")
                print(f"To: {data.get('Destination', 'N/A')}")

                # Display schedule in tabular format
                if "Route" in data:
                    print("\nTrain Schedule:")
                    headers = ["Station", "Arrival", "Departure", "Distance", "Day", "Platform"]
                    route = []
                    for station in data["Route"]:
                        route.append([
                            f"{station.get('StationName', 'N/A')} ({station.get('StationCode', 'N/A')})",
                            station.get("ArrivalTime", "N/A"),
                            station.get("DepartureTime", "N/A"),
                            station.get("Distance", "N/A"),
                            station.get("Day", "N/A"),
                            station.get("Platform", "N/A")
                        ])
                    print(tabulate(route, headers=headers, tablefmt="grid"))
            else:
                print(f"Error: {data.get('Message', 'Unknown error')}")
        except requests.exceptions.RequestException as re:
            print(f"Network error: {str(re)}")
            print("Please check your internet connection and try again.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def search_trains_between_stations(self, src, dst, date):
        """Search for trains between source and destination stations on a given date"""
        print(f"\nSearching trains from {src} to {dst} on {date}...")
        try:
            # Validate date format
            try:
                datetime.strptime(date, "%d-%m-%Y")
            except ValueError:
                print("Invalid date format. Please use DD-MM-YYYY format.")
                return

            # Make API request for trains between stations
            url = f"{self.BASE_URL}/TrainBetweenStations/apikey/{self.API_KEY}/From/{src}/To/{dst}/"
            response = requests.get(url)
            data = response.json()

            # Check if the response is a success
            if str(data.get("ResponseCode")) == "200":
                # Display trains in tabular format
                trains = data.get("Trains", [])
                if trains:
                    headers = ["Train No.", "Name", "Departure", "Arrival", "Duration", "Classes"]
                    trains_data = []
                    for train in trains:
                        # Format classes available
                        classes = ", ".join([c.get("Name", "") for c in train.get("TrainClassList", [])])

                        trains_data.append([
                            train.get("TrainNo", "N/A"),
                            train.get("TrainName", "N/A"),
                            train.get("DepartureTime", "N/A"),
                            train.get("ArrivalTime", "N/A"),
                            train.get("Duration", "N/A"),
                            classes
                        ])

                    print(f"\nTrains from {src} to {dst} on {date}:")
                    print(tabulate(trains_data, headers=headers, tablefmt="grid"))
                else:
                    print(f"No trains found between {src} and {dst} on {date}")
            else:
                print(data.get("ResponseCode"))
                print(f"Error: {data.get('Message', 'Unknown error')}")
        except requests.exceptions.RequestException as re:
            print(f"Network error: {str(re)}")
            print("Please check your internet connection and try again.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def check_train_fare(self):
        """Check fare for a train journey"""
        print("\nCheck Train Fare")
        try:
            # Get inputs
            train_no = input("Enter Train Number: ")
            src = input("Enter Source Station Code: ").upper()
            dst = input("Enter Destination Station Code: ").upper()
            date = input("Enter Date of Journey (DD-MM-YYYY): ")
            travel_quota = input("Enter Quota (e.g., GN, CK): ").upper()

            # Display a processing message
            print(f"\nChecking fare for Train {train_no} from {src} to {dst} in {travel_quota} class...")

            # Make API request for fare
            url = f"{self.BASE_URL}/CheckFare/apikey/{self.API_KEY}/TrainNumber/{train_no}/From/{src}/To/{dst}/Quota/{travel_quota}"
            response = requests.get(url)
            data = response.json()

            # Check if the response is a success
            if str(data.get("ResponseCode")) == "200":
                # Display fare details
                print("\n" + "=" * 60)
                print(f"Train: {data.get('TrainName', 'N/A')} ({train_no})")
                print(f"Journey: {src} to {dst}")
                print(f"Class: {travel_quota}")
                print(f"Date: {date}")
                print(f"\nFare: ₹{data.get('Fare', 'N/A')}")
                if "FareBreakup" in data:
                    print("\nFare Breakup:")
                    for item in data["FareBreakup"]:
                        print(f"  {item.get('Name', '')}: ₹{item.get('Amount', 'N/A')}")
            else:
                print(f"Error: {data.get('Message', 'Unknown error')}")
        except requests.exceptions.RequestException as re:
            print(f"Network error: {str(re)}")
            print("Please check your internet connection and try again.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def check_seat_availability(self):
        """Check seat availability for a train"""
        print("\nCheck Seat Availability")
        try:
            # Get inputs
            train_no = input("Enter Train Number: ")
            src = input("Enter Source Station Code: ").upper()
            dst = input("Enter Destination Station Code: ").upper()
            date = input("Enter Date of Journey (DD-MM-YYYY): ")
            travel_class = input("Enter Class (e.g., SL, 3A, 2A, 1A): ").upper()
            quota = input("Enter Quota (GN for General) (Only GN available): ").upper()

            # Display a processing message
            print(f"\nChecking seat availability for Train {train_no} from {src} to {dst} in {travel_class} class...")

            # Make API request for seat availability
            url = f"{self.BASE_URL}/SeatAvailability/apikey/{self.API_KEY}/TrainNumber/{train_no}/From/{src}/To/{dst}/Date/{date}/Quota/{quota}/Class/{travel_class}/"
            response = requests.get(url)
            data = response.json()

            # Check if the response is a success
            if str(data.get("ResponseCode")) == "200":
                # Display availability details
                print("\n" + "=" * 60)
                print(f"Train: {data.get('TrainName', 'N/A')} ({train_no})")
                print(f"From: {src} to {dst}")
                print(f"Class: {travel_class}, Quota: {quota}")
                print(f"Date: {date}")

                if "AvailabilityStatus" in data:
                    availability = data.get("AvailabilityStatus", "N/A")
                    print(f"\nAvailability: {availability}")

                    # Display fare if available
                    if "Fare" in data:
                        print(f"Fare: ₹{data.get('Fare', 'N/A')}")
                else:
                    print("\nNo availability information found.")
            else:
                print(f"Error: {data.get('Message', 'Unknown error')}")
        except requests.exceptions.RequestException as re:
            print(f"Network error: {str(re)}")
            print("Please check your internet connection and try again.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")


def main():
    """Main function to run the IRCTC application"""
    try:
        IRCTC()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user. Thank you for using IRCTC Train Management System!")
    except Exception as e:
        print(f"\nFatal error: {str(e)}")
        print("Application will exit now.")
        sys.exit(1)


if __name__ == "__main__":
    main()
