openapi: 3.0.3
info:
  title: 401(k) Plan Data API
  description: Async endpoint returning account balance, recent transactions, and investment allocations.
  version: 1.0.0
servers:
  - url: http://localhost:5000
    description: Local development
paths:
  /api/plan:
    get:
      summary: Retrieve plan data
      description: Returns account summary, transaction history, and investment mix. Simulates 1.5 s delay.
      operationId: getPlanData
      tags:
        - Plan
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PlanData'
        '500':
          description: Internal server error
components:
  schemas:
    AccountData:
      type: object
      required:
        - totalBalance
        - vestedBalance
        - ytdChange
        - rateOfReturn
        - lastContributionAmount
        - nextContributionDate
        - contributionRate
      properties:
        totalBalance:
          type: number
          format: double
          example: 142567.89
        vestedBalance:
          type: number
          format: double
          example: 139850.45
        ytdChange:
          type: number
          format: double
          example: 12450.5
        rateOfReturn:
          type: number
          format: double
          example: 12.4
        lastContributionAmount:
          type: number
          format: double
          example: 850.0
        nextContributionDate:
          type: string
          format: date
          example: "2024-06-15"
        contributionRate:
          type: integer
          example: 8
          description: Contribution percentage

    Transaction:
      type: object
      required:
        - id
        - date
        - description
        - amount
        - type
      properties:
        id:
          type: string
          example: "1"
        date:
          type: string
          format: date
          example: "2024-06-01"
        description:
          type: string
          example: "Contribution - Pay Period 11"
        amount:
          type: number
          format: double
          example: 850.0
        type:
          type: string
          enum: [Contribution, Dividend, Fee]
          example: Contribution

    Investment:
      type: object
      required:
        - name
        - ticker
        - balance
        - allocationPercentage
      properties:
        name:
          type: string
          example: "Target Date 2060 Fund"
        ticker:
          type: string
          example: FDKLX
        balance:
          type: number
          format: double
          example: 64155.55
        allocationPercentage:
          type: integer
          example: 45
          description: Allocation percentage

    PlanData:
      type: object
      properties:
        accountData:
          $ref: '#/components/schemas/AccountData'
        transactions:
          type: array
          items:
            $ref: '#/components/schemas/Transaction'
        investments:
          type: array
          items:
            $ref: '#/components/schemas/Investment'