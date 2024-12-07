import pandas as pd


def total_attendees_by_event(attendee_data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the total number of attendees for each event.

    Parameters:
        attendee_data (pd.DataFrame): DataFrame with attendee information.
                                      Columns: ['event_name', 'attendee_id']

    Returns:
        pd.DataFrame: DataFrame with columns ['event_name', 'total_attendees']
    """
    total_attendees = attendee_data.groupby('event_name')['attendee_id'].count().reset_index()
    total_attendees.rename(columns={'attendee_id': 'total_attendees'}, inplace=True)
    return total_attendees.sort_values(by='total_attendees', ascending=False)


def attendees_trend_over_time(attendee_data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the number of attendees over time.

    Parameters:
        attendee_data (pd.DataFrame): DataFrame with attendee information.
                                      Columns: ['rsvp_date', 'attendee_id']

    Returns:
        pd.DataFrame: DataFrame with columns ['rsvp_month', 'total_attendees']
    """
    # Convert 'rsvp_date' to datetime and extract the month
    attendee_data['rsvp_date'] = pd.to_datetime(attendee_data['rsvp_date'])
    attendee_data['rsvp_month'] = attendee_data['rsvp_date'].dt.to_period('M')
    attendees_trend = attendee_data.groupby('rsvp_month')['attendee_id'].count().reset_index()
    attendees_trend.rename(columns={'attendee_id': 'total_attendees'}, inplace=True)
    return attendees_trend


def top_event_by_attendees(attendee_data: pd.DataFrame) -> tuple:
    """
    Find the event with the highest number of attendees.

    Parameters:
        attendee_data (pd.DataFrame): DataFrame with attendee information.
                                      Columns: ['event_name', 'attendee_id']

    Returns:
        tuple: (event_name, total_attendees)
    """
    total_attendees = attendee_data.groupby('event_name')['attendee_id'].count().reset_index()
    top_event = total_attendees.sort_values(by='attendee_id', ascending=False).iloc[0]
    return top_event['event_name'], top_event['attendee_id']
