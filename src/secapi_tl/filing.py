from __future__ import annotations
from datetime import datetime


class Filing:
    """
    The filing class contains all the metadata of a filing.
    It is used to store the filings metadata in a uniform format.
    """

    def __init__(self,
                 accession_number: str = None,
                 filing_date: datetime.date = None,
                 report_date: datetime.date = None,
                 acceptance_date_time: datetime = None,
                 act: str = None,
                 form: str = None,
                 file_number: str = None,
                 film_number: str = None,
                 items: str = None,
                 size: int = None,
                 is_xbrl: bool = None,
                 is_inline_xbrl: bool = None,
                 primary_document: str = None,
                 primary_doc_description: str = None):
        """
        :param accession_number: the accession number of the filing
        :param filing_date: the date the filing was submitted
        :param report_date: the date the filing is reporting
        :param acceptance_date_time: the date and time the filing was accepted
        :param act: the act of the filing
        :param form: the form of the filing
        :param file_number: the file number of the filing
        :param film_number: the film number of the filing
        :param items: the items of the filing
        :param size: the size of the filing
        :param is_xbrl: if the filing is xbrl
        :param is_inline_xbrl: if the filing is inline xbrl
        :param primary_document: the primary document of the filing
        :param primary_doc_description: the primary document description of the filing
        """
        self._accession_number: str = accession_number
        self._filing_date: datetime.date = filing_date
        self._report_date: datetime.date = report_date
        self._acceptance_date_time: datetime = acceptance_date_time
        self._act: str = act
        self._form: str = form
        self._file_number: str = file_number
        self._film_number: str = film_number
        self._items: str = items
        self._size: int = size
        self._is_xbrl: bool = is_xbrl
        self._is_inline_xbrl: bool = is_inline_xbrl
        self._primary_document: str = primary_document
        self._primary_doc_description: str = primary_doc_description

    @staticmethod
    def from_dict(accession_number: str = None,
                  filing_date: str = None,
                  report_date: str = None,
                  acceptance_date_time: str = None,
                  act: str = None,
                  form: str = None,
                  file_number: str = None,
                  film_number: str = None,
                  items: str = None,
                  size: int = None,
                  is_xbrl: str = None,
                  is_inline_xbrl: str = None,
                  primary_document: str = None,
                  primary_doc_description: str = None,
                  ) -> Filing:
        """
        Creates a filing object from the json that is returned by the web request to the sec server.
        The values are converted to appropriate python types.
        """
        accession_number: str = accession_number
        filing_date: datetime.date = datetime.strptime(filing_date, '%Y-%m-%d').date()
        report_date: datetime.date = datetime.strptime(report_date, '%Y-%m-%d').date()
        datetime_str = acceptance_date_time
        datetime_str = datetime_str.replace("T", " ")
        datetime_str = datetime_str.replace(".000Z", "")
        acceptance_date_time: datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        act: str = act
        form: str = form
        file_number: str = file_number
        film_number: str = film_number
        items: str = items
        size: int = size
        is_xbrl: bool = bool(is_xbrl)
        is_inline_xbrl: bool = bool(is_inline_xbrl)
        primary_document: str = primary_document
        primary_doc_description: str = primary_doc_description

        return Filing(accession_number=accession_number,
                      filing_date=filing_date,
                      report_date=report_date,
                      acceptance_date_time=acceptance_date_time,
                      act=act,
                      form=form,
                      file_number=file_number,
                      film_number=film_number,
                      items=items,
                      size=size,
                      is_xbrl=is_xbrl,
                      is_inline_xbrl=is_inline_xbrl,
                      primary_document=primary_document,
                      primary_doc_description=primary_doc_description)
