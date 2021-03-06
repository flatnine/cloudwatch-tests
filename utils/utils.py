from datetime import datetime, timedelta

SIX_WEEKS_AGO = datetime.now() - timedelta(days=42)
ONE_MONTH_AGO = datetime.now() - timedelta(days=28)
ONE_MONTH = 28


def calculate_average_temp(min, max):
    return round((min + max) / 2, 2)


def transpose_date(date, days):
    """ Cloudwatch requires data within last two weeks """
    return date + timedelta(days=days)


def parse_line(row, limit=False, transpose=False):
    """ Extract data from a row, it limit is setup restrict data to 2 weeks
        is transpose is set map data forward two weeks.  Data is only recorded up to last month and
        cloudwatch events only stores data for the last 2 weeks."""

    line = {}
    parsed_date = datetime.strptime(row[0], '%d-%b-%Y')
    if limit:
        if parsed_date < SIX_WEEKS_AGO or parsed_date > ONE_MONTH_AGO:
            return

    if transpose:
        line['date'] = transpose_date(parsed_date, ONE_MONTH)
    else:
        line['date'] = parsed_date

    try:
        min_temp = float(row[4])
        max_temp = float(row[2])
    except ValueError:
        print('{row[4]} {row[2]} Cant be converted on {parsed_date}')
        min_temp = -273.15
        max_temp = -273.15
    line['average_temp'] = calculate_average_temp(min_temp, max_temp)
    return line
