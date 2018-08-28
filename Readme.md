# Amazon reviews parser

Parsing reviews by item ID from Amazon site, then dumping them in json array with such structure:
```json
[
  {
    "brand": "WonderWoof",
    "url": "https://www.amazon.com/dp/B00WKZG692",
    "reviews": [
      {
        "review_url": "https://www.amazon.com/gp/customer-reviews/R3BUOU7SCYQCYL",
        "title": "Great Product for pet lovers",
        "stars": 4,
        "is_avp": false,
        "helpful_for": 0,
        "date": "July 25, 2017",
        "text": "We love our Whistle!! It gives us peace of mind 24/7. Wonderful customer service!"
      }
    ]
  }
]
```

`is_avp` - Purchase made by Verified Customer `true`/`false`

Other keys are pretty straightforward.


