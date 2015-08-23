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
    }

##NOTES
[GET] /notes/search 

    Request: 
    {
        sort: "recent" OR "popular" OR  "distance"
        filter: "all" OR "timeLimitOnly" OR "takesLimitOnly"
        lat: 444
        lon:444
        radius: "small" OR "medium" OR "large"
        search:"cute dogs"
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
        limit:200
        tags:["dog","funny"]
        has_time_limit : true 
        has_take_limit : true 
    }]


[POST] /notes
  
    Request: 
    {
        author.id : 34242424234
        message:"There is a cute dog in the place"
        media:"http://img.wigo/5242424.png"
        lat:47.3590900
        lon:3.3852100
        expiration:2014-08-23T18:05:46Z OR None 
        limit:200  # 0 or None
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
        limit:200
        tags:["dog","funny"]
        has_time_limit : true 
        has_take_limit : true 

    }


[DELETE] /notes/id
    
    Request: {}
    Response:{}

##COMMENTS

[GET] /notes/{id}/comments/
    
    Request: {}


    Response:[{
        comment:"This is my commentaire"
        author.name:"ikit"
        author.avatar:"http://gravatar..."
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
    }

[GET] /tags
    
    Request: {
        lat :43.82186
        lon:-79.42456
        radius: 50
    }

    Response:{
    [
    "name":"dog"
    "count":25
    ]
    }
  


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

[GET] /users/{id}/takes
[GET] /users/{id}/notes

    Request: {}

    Response:{
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
        limit:200
        tags:["dog","funny"]
        has_time_limit : true 
        has_take_limit : true 

        ref: 54242403242
        code:213123131312312312324234324

    }


WEBSOCKETS : 
ws://notification/subscribe

    Request : {TAGS}
    Response: Done

ws://notification/send

    Request : {POSITION}
    Response: {NOTES ID}





