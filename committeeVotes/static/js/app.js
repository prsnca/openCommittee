var app = angular.module('openCommitteeApp', ['ui.router']);

app.config(function ($stateProvider, $urlRouterProvider) {
    // For any unmatched url, send to /route1
    $urlRouterProvider.otherwise("/");
    $stateProvider
        .state('index', {

            url: "/",
            templateUrl: "/static/html/index.html",
            resolve: {
                bills:
                    function($http) {
                        return $http({method: 'GET', url: '/api/bills'})
                           .then (function (res) {
                               return res.data.results;
                           });
                    },
                ministers:
                    function($http) {
                        return $http({method: 'GET', url: '/api/ministers'})
                           .then (function (res) {
                               return res.data.results;
                           });
                    }
            },
            controller: 'mainCtrl'
        })
});

app.controller('mainCtrl', ['$scope','bills','ministers',
function ($scope, bills) {
    $scope.bills = bills;
    $scope.ministers = ministers;

}]);


app.config(function($interpolateProvider)
{
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
});/**
 * Created by Yaron on 7/27/15.
 */
