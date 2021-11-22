class ExecutionStatus:
    
    _id: str
    _status: str
    _output: str
    _error: str

    def __init__(self, _id_arg, _status_arg, _output_arg, _error_arg) -> None:
        self._id = _id_arg
        self._status = _status_arg
        self._output = _output_arg
        self._error = _error_arg

    def to_dict( self):
        res = {}
        if self._status is not None:
            res['_status'] = self._status
        if self._output is not None:
            res['_output'] = self._output
        if self._error is not None:
            res['_error'] = self._error
        return res

    @staticmethod
    def from_dict(ob_map):
        _id = None
        _status = None
        _output = None
        _error = None
        if '_id' in ob_map:
            _id = ob_map['_id']
        if '_status' in ob_map:
            _status = ob_map['_status']
        if '_output' in ob_map:
            _output = ob_map['_output']
        if '_error' in ob_map:
            _error = ob_map['_error']
        return ExecutionStatus( _id, _status, _output, _error)
