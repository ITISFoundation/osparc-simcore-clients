# JobStatus

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**job_id** | **str** |  |
**state** | [**TaskStates**](TaskStates.md) |  |
**progress** | **int** |  | [optional] [default to 0]
**submitted_at** | **datetime** |  |
**started_at** | **datetime** | Timestamp that indicate the moment the solver starts execution or None if the event did not occur | [optional]
**stopped_at** | **datetime** | Timestamp at which the solver finished or killed execution or None if the event did not occur | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API Classes]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
