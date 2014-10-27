==MODELS==
Config model contains different kind of static parameters.
    
    Config {
        allowed_radius    [list]15meter, 20 meter ...
        message_length    [int] maximum message length
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
        limit.current   [int] The current count of tooks
        limit.max       [int] The maximum allowed tooks. -1 means infinite
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

== ENDPOINT ==

=== CONFIG ===

[GET] /config/

    Request:{}

    Response:
    {
    allowed_radius      : [15,20,60,100]
    message_length      : 255   
    version             : 1.0      
    }

=== NOTES ===

[GET] /notes/search 

    Request: 
    {
        order: ["recent","popular"]
        radius: 50
        search:"cute dogs"
    }

Response:

    Body: [{
        author.name: "ikit"
        author.avatar: "http://gravatar.png"
        anonymous:true
        message:"There is a cute dog in the place"
        picture:"http://img.wigo/5242424.png"
        timestamp:2014-08-23T18:05:46Z
        location:[47.3590900,3.3852100]
        expiration:2014-08-23T18:05:46Z
        limit.current: 143
        limit.max:200
        tags:["dog","funny"]
    }]


[POST] /notes
  
    Request: 
    {
        author.id : 34242424234
        anonymous:true
        message:"There is a cute dog in the place"
        picture:"http://img.wigo/5242424.png"
        location:[47.3590900,3.3852100]
        expiration:2014-08-23T18:05:46Z
        limit.max:200
    }

    Response:{}

[GET] /notes/{id}

    Request: {}
   
    Body: {
        author.name: "ikit"
        author.avatar: "http://gravatar.png"
        anonymous:true
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

===COMMENTS ===

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
        radius: 50
    }

    Response:{
    tags: ["apple","dog","cute"]
    }
  


=== USER ===

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

Summary : 
[GET] /config/
[GET] /notes/search 
[GET] /notes/{id}
[DELETE] /notes/id
[GET] /notes/{id}/comments/
[POST] /notes/{id}/comments/
[DELETE] /comments/{id}
[GET] /comments/{id}
[GET] /tags
[GET] /users/{id}
[UPDATE] /users/{id}
[POST] /users/login
[POST] /users/logout
[GET]  /users/me
[GET] /users/{id}/pockets
[POST] /users/
[GET] /users/{id}/pockets








