import copy
import datetime
import json
import logging
import os.path
import tempfile
import unittest
import uuid

from pbcommand.models import FileTypes, DataStore, DataStoreFile, PacBioAlarm
from pbcommand.models.common import _datetime_to_string

log = logging.getLogger(__name__)


class TestLoadFileTypes(unittest.TestCase):

    def test_file_types(self):
        # smoke test for loading file types
        ft = FileTypes.DS_ALIGN
        self.assertIsNotNone(ft)
        self.assertEqual(ft, copy.deepcopy(FileTypes.DS_ALIGN))
        self.assertNotEqual(ft, FileTypes.DS_ALIGN_CCS)

    def test_is_valid(self):
        ft = FileTypes.DS_ALIGN
        self.assertTrue(FileTypes.is_valid_id(ft.file_type_id))


class TestDataStore(unittest.TestCase):

    def test_datastore_file(self):
        tmpfile = tempfile.NamedTemporaryFile(suffix=".subreadset.xml").name
        ds = DataStoreFile(str(uuid.uuid4()),
                           "pbcommand.tasks.dev_task",
                           FileTypes.DS_SUBREADS.file_type_id,
                           tmpfile,
                           False,
                           "Subreads",
                           "Subread DataSet XML")
        log.info("DataStoreFile: {s}".format(s=ds))
        ds2 = DataStoreFile.from_dict(ds.to_dict())
        for attr in ["uuid", "file_type_id", "file_id",
                     "path", "is_chunked", "name", "description"]:
            self.assertEqual(getattr(ds2, attr), getattr(ds, attr))
        self.assertEqual(ds.file_type, FileTypes.DS_SUBREADS)

    def test_datastore_paths(self):
        tmpfile = tempfile.NamedTemporaryFile(suffix=".subreadset.xml").name
        base_dir = os.path.dirname(tmpfile)
        tmp_ds = os.path.join(base_dir, "datastore.json")
        dsf = DataStoreFile(str(uuid.uuid4()),
                            "pbcommand.tasks.dev_task",
                            FileTypes.DS_SUBREADS.file_type_id,
                            os.path.basename(tmpfile),
                            False,
                            "Subreads",
                            "Subread DataSet XML")
        ds = DataStore([dsf])
        ds.write_json(tmp_ds)
        with open(tmp_ds) as json_in:
            d = json.loads(json_in.read())
            self.assertFalse(os.path.isabs(d['files'][0]['path']))
        ds = DataStore.load_from_json(tmp_ds)
        self.assertEqual(list(ds.files.values())[0].path, tmpfile)


class TestAlarm(unittest.TestCase):

    def test_pacbio_alarm(self):
        json_tmp = tempfile.NamedTemporaryFile(suffix=".json").name
        d = {
            "exception": "IOError",
            "info": "this would usually be a Python traceback",
            "message": "Something broke!",
            "name": "IOError",
            "severity": "ERROR",
            "owner": "python",
            "createdAt": _datetime_to_string(datetime.datetime.now()),
            "id": str(uuid.uuid4())
        }
        a = PacBioAlarm.from_dict(d)
        self.assertEqual(a.log_level, logging.ERROR)
        a.to_json(json_tmp)
        a = PacBioAlarm.from_json(json_tmp)
        self.assertEqual(a.log_level, logging.ERROR)
