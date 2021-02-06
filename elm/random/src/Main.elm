module Main exposing (..)

import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Random


main =
    Browser.element
        { init = init
        , view = view
        , update = update
        , subscriptions = subscriptions
        }


type alias Model =
    { x : Int
    , y : Int
    }


type Msg
    = Clicked
    | NewPosition ( Int, Int )


init : () -> ( Model, Cmd Msg )
init _ =
    ( Model 50 100, Cmd.none )


positionGenerator : Random.Generator ( Int, Int )
positionGenerator =
    Random.map2 Tuple.pair
        (Random.int 50 350)
        (Random.int 50 350)


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Clicked ->
            ( model
            , Random.generate NewPosition positionGenerator
            )

        NewPosition ( x, y ) ->
            ( Model x y
            , Cmd.none
            )


subscriptions : Model -> Sub Msg
subscriptions _ =
    Sub.none


view : Model -> Html Msg
view model =
    button
        [ style "position" "absolute"
        , style "top" (String.fromInt model.x ++ "px")
        , style "left" (String.fromInt model.y ++ "px")
        , onClick Clicked
        ]
        [ text "Click me!" ]
