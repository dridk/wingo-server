#MODELS
Config model contains different kind of static parameters.
    
    Config {
        allowed_radius    [list]15meter, 20 meter ...
        max_note_length    [int] maximum message length
    }

Notes model contains all data for each footprint. *limit.max* is the pocket tool limit. *limit.current* is the actual count of total amount of tooks.

    Notes {
        id              [key]
        author          [index]
        anonymous       [bool]
        message         [text]
        picture         [url]
        timestamp       [time]
        location        [Point]
        expiration      [Date]
        takes           [int] The current count of tooks
        limit           [int] The maximum allowed tooks. -1 means infinite
        tags            [list]Tags from text,to perform search
    }

User is the model which contains data about user. It contains a particular field called pockets, which is a copy from *Notes* and represent the Poket.

    User {
        id          [key]
        email       [string]
        password    [string]
        nickname    [string]
        pockets     [list of Pokets Notes + extra]
            ref     [Id to Notes]
            code    [Uniq Code : Id + privatekey to use for QRCode]
    }

Comments is the the comments...

    Comments {
        id              [key]
        note_id         [key]
        comment         [String]
        author          [key]
    }

#ENDPOINT
##CONFIG
[GET] /config/

    Request:{}

    Response:
    {
    allowed_radius      : [15,20,60,100]
    max_note_length     : 255   
    version             : 1.0      
    }

##NOTES
[GET] /notes/search 

    Request: 
    {
        order: ["recent","popular"]
        lat: 444
        lon:444
        radius: 50
        search:"cute dogs"
    }

    Response:
    Body: [{
        author.name: "ikit"
        author.avatar: "http://gravatar.png"
        anonymous:true
        lat:43.4535
        lon:-4.4345
        message:"There is a cute dog in the place"
        picture:"http://img.wigo/5242424.png"
        timestamp:2014-08-23T18:05:46Z
        location:[47.3590900,3.3852100]
        expiration:2014-08-23T18:05:46Z
        takes: 143
        limit:200
        tags:["dog","funny"]
    }]


[POST] /notes
  
    Request: 
    {
        author.id : 34242424234
        anonymous:true
        message:"There is a cute dog in the place"
        picture:"http://img.wigo/5242424.png"
        lat:47.3590900
        lon:3.3852100
        expiration:2014-08-23T18:05:46Z
        limit:200
    }

    Response:{}

[GET] /notes/{id}

    Request: {}
   
    Body: {
        author.name: "ikit"
        author.avatar: "http://gravatar.png"
        anonymous:true
        lat:43.4535
        lon:-4.4345
        message:"There is a cute dog in the place"
        picture:"http://img.wigo/5242424.png"
        timestamp:2014-08-23T18:05:46Z
        location:[47.3590900,3.3852100]
        expiration:2014-08-23T18:05:46Z
        limit.current: 143
        limit.max:200
        tags:["dog","funny"]

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

[GET] /tags
    
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

[GET] /users/{id}

    Request: {}

    Response:{
        email : ikit@glandeur.fr
        nickname:ikit
        pocket_count: 43
    }

[GET] /users/{id}/pockets

    Request: {}

    Response:{
        author.name: "ikit"
        author.avatar: "http://gravatar.png"
        anonymous:true
        lat:43.4535
        lon:-4.4345
        message:"There is a cute dog in the place"
        picture:"http://img.wigo/5242424.png"
        timestamp:2014-08-23T18:05:46Z
        location:[47.3590900,3.3852100]
        expiration:2014-08-23T18:05:46Z
        limit.current: 143
        limit.max:200
        tags:["dog","funny"]
        ref: 54242403242
        code:213123131312312312324234324

    }


[GET] /places?lat=40.74917,-73.98529

Request: {}

    Response:{
        address : "43 rue des acadiens"
        map : "http://here.truc.fr"
    }


Summary : 
[GET] /config/
notes/search?lat=40.74917&lon=-73.98529&order=recent&radius=50&query=cute dogs
[GET] /notes/{id}
[DELETE] /notes/id
[GET] /notes/{id}/comments/
[POST] /notes/{id}/comments/
[DELETE] /comments/{id}
[GET] /comments/{id}
[GET] /tags?radius=50
[GET] /users/{id}
[UPDATE] /users/{id}
[POST] /users/login
[POST] /users/logout
[GET]  /users/me
[GET] /users/{id}/pockets
[POST] /users/
[GET] /users/{id}/pockets











