# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

import vlq_base128_le
class OsuDb(KaitaiStruct):
    """osu!.db file format in rhythm game osu!,
    the legacy DB file structure used in the old osu stable client (not lazer).
    
    DB files are in the `osu-stable` installation directory:
    Windows: `%localappdata%\osu!`
    Mac OSX: `/Applications/osu!.app/Contents/Resources/drive_c/Program Files/osu!/`
    
    Unless otherwise specified, all numerical types are stored little-endian.
    Integer values, including bytes, are all unsigned.
    UTF-8 characters are stored in their canonical form, with the higher-order byte first.
    
    osu!.db contains a cached version of information about all currently installed beatmaps.
    Deleting this file will force osu! to rebuild the cache from scratch.
    This may be useful since it may fix certain discrepancies, such as beatmaps
    that had been deleted from the Songs folder but are still showing up in-game.
    Unsurprisingly, due to its central role in the internal management of beatmaps
    and the amount of data that is cached, osu!.db is the largest of the .db files.
    
    .. seealso::
       Source - https://github.com/ppy/osu/wiki/Legacy-database-file-structure
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.osu_version = self._io.read_u4le()
        self.folder_count = self._io.read_u4le()
        self.account_unlocked = OsuDb.Bool(self._io, self, self._root)
        self.account_unlock_date = self._io.read_u8le()
        self.player_name = OsuDb.String(self._io, self, self._root)
        self.num_beatmaps = self._io.read_u4le()
        self.beatmaps = [None] * (self.num_beatmaps)
        for i in range(self.num_beatmaps):
            self.beatmaps[i] = OsuDb.Beatmap(self._io, self, self._root)

        self.user_permissions = self._io.read_u4le()

    class TimingPoint(KaitaiStruct):
        """Consists of a Double, signifying the BPM, another Double,
        signifying the offset into the song, in milliseconds, and a Boolean;
        if false, then this timing point is inherited.
        See https://osu.ppy.sh/wiki/osu!_File_Formats/Osu_(file_format)
        for more information regarding timing points.
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.bpm = self._io.read_f8le()
            self.offset = self._io.read_f8le()
            self.not_inherited = OsuDb.Bool(self._io, self, self._root)


    class String(KaitaiStruct):
        """Has three parts; a single byte which will be either 0x00, indicating that
        the next two parts are not present, or 0x0b (decimal 11), indicating that
        the next two parts are present.
        If it is 0x0b, there will then be a ULEB128, representing the byte length
        of the following string, and then the string itself, encoded in UTF-8.
        See https://en.wikipedia.org/wiki/UTF-8.
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.is_present = self._io.read_u1()
            if self.is_present == 11:
                self.len_str = vlq_base128_le.VlqBase128Le(self._io)

            if self.is_present == 11:
                self.value = (self._io.read_bytes(self.len_str.value)).decode(u"UTF-8")



    class Beatmap(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            if self._root.osu_version < 20191106:
                self.len_beatmap = self._io.read_u4le()

            self.artist_name = OsuDb.String(self._io, self, self._root)
            self.artist_name_unicode = OsuDb.String(self._io, self, self._root)
            self.song_title = OsuDb.String(self._io, self, self._root)
            self.song_title_unicode = OsuDb.String(self._io, self, self._root)
            self.creator_name = OsuDb.String(self._io, self, self._root)
            self.difficulty = OsuDb.String(self._io, self, self._root)
            self.audio_file_name = OsuDb.String(self._io, self, self._root)
            self.md5_hash = OsuDb.String(self._io, self, self._root)
            self.osu_file_name = OsuDb.String(self._io, self, self._root)
            self.ranked_status = self._io.read_u1()
            self.num_hitcircles = self._io.read_u2le()
            self.num_sliders = self._io.read_u2le()
            self.num_spinners = self._io.read_u2le()
            self.last_modification_time = self._io.read_u8le()
            _on = self._root.osu_version < 20140609
            if _on == True:
                self.approach_rate = self._io.read_u1()
            elif _on == False:
                self.approach_rate = self._io.read_f4le()
            _on = self._root.osu_version < 20140609
            if _on == True:
                self.circle_size = self._io.read_u1()
            elif _on == False:
                self.circle_size = self._io.read_f4le()
            _on = self._root.osu_version < 20140609
            if _on == True:
                self.hp_drain = self._io.read_u1()
            elif _on == False:
                self.hp_drain = self._io.read_f4le()
            _on = self._root.osu_version < 20140609
            if _on == True:
                self.overall_difficulty = self._io.read_u1()
            elif _on == False:
                self.overall_difficulty = self._io.read_f4le()
            self.slider_velocity = self._io.read_f8le()
            if self._root.osu_version >= 20140609:
                _on = self._root.osu_version <= 20250107
                if _on == True:
                    self.star_rating_osu = OsuDb.IntDoublePairs(self._io, self, self._root)
                elif _on == False:
                    self.star_rating_osu = OsuDb.IntFloatPairs(self._io, self, self._root)

            if self._root.osu_version >= 20140609:
                _on = self._root.osu_version <= 20250107
                if _on == True:
                    self.star_rating_taiko = OsuDb.IntDoublePairs(self._io, self, self._root)
                elif _on == False:
                    self.star_rating_taiko = OsuDb.IntFloatPairs(self._io, self, self._root)

            if self._root.osu_version >= 20140609:
                _on = self._root.osu_version <= 20250107
                if _on == True:
                    self.star_rating_ctb = OsuDb.IntDoublePairs(self._io, self, self._root)
                elif _on == False:
                    self.star_rating_ctb = OsuDb.IntFloatPairs(self._io, self, self._root)

            if self._root.osu_version >= 20140609:
                _on = self._root.osu_version <= 20250107
                if _on == True:
                    self.star_rating_mania = OsuDb.IntDoublePairs(self._io, self, self._root)
                elif _on == False:
                    self.star_rating_mania = OsuDb.IntFloatPairs(self._io, self, self._root)

            self.drain_time = self._io.read_u4le()
            self.total_time = self._io.read_u4le()
            self.audio_preview_start_time = self._io.read_u4le()
            self.timing_points = OsuDb.TimingPoints(self._io, self, self._root)
            self.difficulty_id = self._io.read_u4le()
            self.beatmap_id = self._io.read_u4le()
            self.thread_id = self._io.read_u4le()
            self.grade_osu = self._io.read_u1()
            self.grade_taiko = self._io.read_u1()
            self.grade_ctb = self._io.read_u1()
            self.grade_mania = self._io.read_u1()
            self.local_beatmap_offset = self._io.read_u2le()
            self.stack_leniency = self._io.read_f4le()
            self.gameplay_mode = self._io.read_u1()
            self.song_source = OsuDb.String(self._io, self, self._root)
            self.song_tags = OsuDb.String(self._io, self, self._root)
            self.online_offset = self._io.read_u2le()
            self.song_title_font = OsuDb.String(self._io, self, self._root)
            self.is_unplayed = OsuDb.Bool(self._io, self, self._root)
            self.last_played_time = self._io.read_u8le()
            self.is_osz2 = OsuDb.Bool(self._io, self, self._root)
            self.folder_name = OsuDb.String(self._io, self, self._root)
            self.last_check_repo_time = self._io.read_u8le()
            self.ignore_sound = OsuDb.Bool(self._io, self, self._root)
            self.ignore_skin = OsuDb.Bool(self._io, self, self._root)
            self.disable_storyboard = OsuDb.Bool(self._io, self, self._root)
            self.disable_video = OsuDb.Bool(self._io, self, self._root)
            self.visual_override = OsuDb.Bool(self._io, self, self._root)
            if self._root.osu_version < 20140609:
                self.unknown_short = self._io.read_u2le()

            self.last_modification_time_int = self._io.read_u4le()
            self.mania_scroll_speed = self._io.read_u1()


    class TimingPoints(KaitaiStruct):
        """An Int indicating the number of following Timing points, then the aforementioned Timing points."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_points = self._io.read_u4le()
            self.points = [None] * (self.num_points)
            for i in range(self.num_points):
                self.points[i] = OsuDb.TimingPoint(self._io, self, self._root)



    class Bool(KaitaiStruct):
        """0x00 for false, everything else is true."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.byte = self._io.read_u1()

        @property
        def value(self):
            if hasattr(self, '_m_value'):
                return self._m_value if hasattr(self, '_m_value') else None

            self._m_value = (False if self.byte == 0 else True)
            return self._m_value if hasattr(self, '_m_value') else None


    class IntDoublePair(KaitaiStruct):
        """The first byte is 0x08, followed by an Int, then 0x0d, followed by a Double.
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic1 = self._io.read_bytes(1)
            if not self.magic1 == b"\x08":
                raise kaitaistruct.ValidationNotEqualError(b"\x08", self.magic1, self._io, u"/types/int_double_pair/seq/0")
            self.mods = self._io.read_u4le()
            self.magic2 = self._io.read_bytes(1)
            if not self.magic2 == b"\x0D":
                raise kaitaistruct.ValidationNotEqualError(b"\x0D", self.magic2, self._io, u"/types/int_double_pair/seq/2")
            self.rating = self._io.read_f8le()


    class IntDoublePairs(KaitaiStruct):
        """An Int indicating the number of following Int-Double pairs, then the aforementioned pairs."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_pairs = self._io.read_u4le()
            self.pairs = [None] * (self.num_pairs)
            for i in range(self.num_pairs):
                self.pairs[i] = OsuDb.IntDoublePair(self._io, self, self._root)



    class IntFloatPair(KaitaiStruct):
        """The first byte is 0x08, followed by an Int, then 0x0c, followed by a Float.
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic1 = self._io.read_bytes(1)
            if not self.magic1 == b"\x08":
                raise kaitaistruct.ValidationNotEqualError(b"\x08", self.magic1, self._io, u"/types/int_float_pair/seq/0")
            self.mods = self._io.read_u4le()
            self.magic2 = self._io.read_bytes(1)
            if not self.magic2 == b"\x0C":
                raise kaitaistruct.ValidationNotEqualError(b"\x0C", self.magic2, self._io, u"/types/int_float_pair/seq/2")
            self.rating = self._io.read_f4le()


    class IntFloatPairs(KaitaiStruct):
        """An Int indicating the number of following Int-Float pairs, then the aforementioned pairs."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_pairs = self._io.read_u4le()
            self.pairs = [None] * (self.num_pairs)
            for i in range(self.num_pairs):
                self.pairs[i] = OsuDb.IntFloatPair(self._io, self, self._root)




