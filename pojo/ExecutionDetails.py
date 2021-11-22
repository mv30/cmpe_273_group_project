class ExecutionDetails:

    _id: str
    _source_code: str
    _input: str

    def __init__( self, _id_arg, _source_code_arg, _input_arg) -> None:
        self._id = _id_arg
        self._source_code = _source_code_arg
        self._input = _input_arg
    
    @staticmethod
    def from_dict( ob_map):
        _id = None
        _source_code = None
        _input = None
        if '_id' in ob_map:
            _id  = ob_map['_id']
        if '_source_code' in ob_map:
            _source_code = ob_map['_source_code']
        if '_input' in ob_map:
            _input = ob_map['_input']
        return ExecutionDetails( _id, _source_code, _input)

    def to_dict( self):
        res = {}
        res['_id'] = self._id
        res['_souce_code'] = self._source_code
        res['_input'] = self._input
        return res