# Wealden Bin Collection Dates Home Assistant Integration

This custom integration for Home Assistant retrieves bin collection dates for a given UPRN from the Wealden District Council website and displays them as sensors in Home Assistant.

## IMPORTANT NOTE

I recommend adjusting the scraping frequency to once a week to avoid being blocked for too many requests. Additionally, consider setting up a separate local proxy cache to further reduce risk.

## Installation

1. Copy the `wealden_bin_collection` directory from this repository into the `custom_components` directory within your Home Assistant configuration directory. If the `custom_components` directory does not exist, create it.

2. Add the following configuration to your `configuration.yaml` file:

```
wealden_bin_collection:
  uprn: YOUR_UPRN_NUMBER
```

Replace `YOUR_UPRN_NUMBER` with your property's UPRN number.

3. Restart Home Assistant.

## Obtaining your UPRN
To find your property's UPRN number, follow these steps:

1. Visit the [Wealden Bin Search page](https://www.wealden.gov.uk/recycling-and-waste/bin-search/).
2. Enter your postcode in the search field and click "Search".
3. Select your house number from the list of addresses.
4. After selecting your house number, the UPRN is appended to the URL in your browser's address bar. It will look like this: `https://www.wealden.gov.uk/recycling-and-waste/bin-search/?uprn=YOUR_UPRN_NUMBER`.

Copy the UPRN number from the URL and use it in your configuration.yaml file as explained in the Installation section above.

## Sensors
The integration creates three sensors for each collection type (black, green, and brown bins):

`sensor.black_bin_collection_date`: Displays the collection date for the black bin (refuse).
`sensor.green_bin_collection_date`: Displays the collection date for the green bin (recycling).
`sensor.brown_bin_collection_date`: Displays the collection date for the brown bin (garden waste).

Each sensor will display the collection date in the format `dd/mm/yyyy` and show an appropriate bin icon.

## Creating an Automation
You can create an automation to send notifications or perform actions based on the bin collection dates. For example, you can set up a notification to remind you about the upcoming bin collection the evening before at 6 PM.

To create an automation using the Home Assistant UI, follow these steps:

1. In the Home Assistant UI, go to "Configuration" > "Automations".
2. Click the "+" button in the bottom right corner to create a new automation.
3. Give your automation a name, for example, "Bin Collection Reminder".
4. Set the trigger type to "Time".
5. In the "At" field, enter the time when you want the notification to be sent, for example, `18:00:00` for 6 PM.
6. Add a condition of type "Template" and use a template to check if the collection date for any of the bins is tomorrow. For example:
`{{ (as_timestamp(now()) + 86400) | timestamp_custom('%d/%m/%Y') in [states('sensor.black_bin_collection_date'), states('sensor.green_bin_collection_date'), states('sensor.brown_bin_collection_date')] }}
`
7. Add an action to send a notification, for example, using the "notify" service. 
```
service: notify.your_device_name
data:
  message: |-
    {% set tomorrow = as_timestamp(now()) + 86400 %} {% set bin_names = {
      states('sensor.black_bin_collection_date'): 'black',
      states('sensor.green_bin_collection_date'): 'green',
      states('sensor.brown_bin_collection_date'): 'brown'
    } %} {% for bin_date, bin_name in bin_names.items() %}
      {% if tomorrow | timestamp_custom('%d/%m/%Y') == bin_date %}
        Put the {{ bin_name }} bin out.
      {% endif %}
    {% endfor %}
  title: Bin day tomorrow!
```