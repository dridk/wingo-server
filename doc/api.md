#ENDPOINT
##CONFIG
[GET] /config/

    Request:{}

    Response:
    {
    radius : {small: 50, medium :500, large : 5000}  
    max_note_length [int] : 255
    version_name : "Thorfinn"
    version : "1.0.0"
    note_per_page : 20 
    debug : false
    }


[GET] /shema/ 


##NOTES
[GET] /notes/ 

    Request: 
    {
        sort:   "recent" OR "popular" OR  "distance" ("recent")
        filter: "all" OR "timeLimitOnly" OR "takesLimitOnly" ("all")
        lat:    444 (required)
        lon:    444  (required)
        radius: "small" OR "medium" OR "large" (small)
        tags:   "cat" (None)
    }

    Response:
    Body: [{
        author.name: "ikit"
        author.avatar: "http://gravatar.png"
        lat:43.4535
        lon:-4.4345
        message:"There is a cute dog in the place"
        media:"http://img.wigo/5242424.png"
        timestamp:2014-08-23T18:05:46Z
        location:[47.3590900,3.3852100]
        expiration:2014-08-23T18:05:46Z
        takes: 143
        takes_limit:200
        tags:["dog","funny"]
        has_time_limit : true 
        has_take_limit : true 
        comment_count  : 43
    }]


[POST] /notes
  
    Request: 
    {
        author.id : 34242424234 ( required )
        message:"There is a cute dog in the place" ( required )
        media:"http://img.wigo/5242424.png" ( None )
        lat:47.3590900 ( required )
        lon:3.3852100  ( required )
        expiration:2014-08-23T18:05:46Z ( None ) 
        limit:200 ( None )
    }

    Response:{}

[GET] /notes/{id}

    Request: {}
   
    Body: {
        author.name: "ikit"
        author.avatar: "http://gravatar.png"
        lat:43.4535
        lon:-4.4345
        message:"There is a cute dog in the place"
        media:"http://img.wigo/5242424.png"
        timestamp:2014-08-23T18:05:46Z
        location:[47.3590900,3.3852100]
        expiration:2014-08-23T18:05:46Z
        takes: 143
        takes_limit:200
        tags:["dog","funny"]
        has_time_limit : true 
        has_take_limit : true 
        comment_count  : 43
    }


[DELETE] /notes/{id}
    
    Request: {}
    Response:{}

##COMMENTS

[GET] /notes/{id}/comments/
    
    Request: {}


    Response:[{
        comment:"This is my commentaire"
        author.name:"ikit"
        author.avatar:"http://gravatar..."
        timestamp : "2014-08-23T18:05:46Z"
    }]


[POST] /notes/{id}/comments/
    
    Request: {
      comment:"This is my commentaire"  
    }

    Response:{}


[DELETE] /comments/{id}
    
    Request: {}

    Response:{}

[GET] /comments/{id}
    
    Request: {}

    Response:{
        comment:"This is my commentaire"
        author.name:"ikit"
        author.avatar:"http://gravatar..."
        timestamp : "2014-08-23T18:05:46Z"

    }

[GET] /tags
    
    Request: {
        lat :43.82186 (required)
        lon:-79.42456 (required)
        radius: "small" OR "medium" OR "large" ("small")
    }

    Response:{
    [{
    "name":"dog"
    "count":25
    }
  
    ]}
  

##USER

[GET] /users/{id}
[GET] /users/me 

    Request: {}

    Response:{
        email : ikit@glandeur.fr
        name:ikit
        takes_count: 43
        notes_count : 43
    }

[GET] /users/{id}/notes
[GET] /users/{id}/pocket

    Request: {}

    Response:[{
        author.name: "ikit"
        author.avatar: "http://gravatar.png"
        lat:43.4535
        lon:-4.4345
        message:"There is a cute dog in the place"
        media:"http://img.wigo/5242424.png"
        timestamp:2014-08-23T18:05:46Z
        location:[47.3590900,3.3852100]
        expiration:2014-08-23T18:05:46Z
        takes: 143
        takes_limit:200
        tags:["dog","funny"]
        has_time_limit : true 
        has_take_limit : true 
        comment_count  : 43

        ref: 54242403242
        code:213123131312312312324234324

    }]


WEBSOCKETS : 
ws://notification/subscribe

    Request : {TAGS}
    Response: Done

ws://notification/send

    Request : {POSITION}
    Response: {NOTES ID}





