aws dynamodb create-table \
  --table-name UserActivityTable \
  --attribute-definitions AttributeName=u,AttributeType=N AttributeName=t,AttributeType=N \
  --key-schema AttributeName=u,KeyType=HASH AttributeName=t,KeyType=RANGE \
  --provisioned-throughput ReadCapacityUnits=5 WriteCapacityUnits=5 \
  --endpoint-url http://localhost:5555 \
  --global-secondary-indexes \
    "IndexName=GSI1,KeySchema=[{AttributeName=u,KeyType=HASH},{AttributeName=day-hour,KeyType=RANGE}],Projection={ProjectionType=INCLUDE,NonKeyAttributes=[v]}" \
  --attribute-definitions AttributeName=v,AttributeType=NS