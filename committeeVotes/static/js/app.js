var app = angular.module('openCommitteeApp', ['ui.router']);

app.config(function ($stateProvider, $urlRouterProvider) {
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
        .state('bills', {
            url: "/bills",
            templateUrl: "/static/html/bills.html",
            resolve: {
                bills:
                    function($http) {
                        return $http({method: 'GET', url: '/api/bills'})
                           .then (function (res) {
                               return res.data.results;
                           });
                    }
            },
            controller: 'billsCtrl'

        })
        .state('bill', {
            url: "/bills/:billId",
            templateUrl: "/static/html/bill.html",
            resolve: {
                bill:
                    function($http, $stateParams) {
                        return $http({method: 'GET', url: '/api/bills/'+$stateParams.billId })
                           .then (function (res) {
                               return res.data;
                           });
                    }
            },
            controller: 'billCtrl'

        })
});

app.controller('mainCtrl', ['$scope','bills','ministers',
function ($scope, bills, ministers) {
    $scope.bills = bills;
    $scope.ministers = ministers;

}]);

app.controller('billsCtrl', ['$scope','bills',
function ($scope, bills) {
    $scope.bills = bills;

}]);

app.controller('billCtrl', ['$scope','bill',
function ($scope, bill) {
    $scope.bill = bill;

}]);


app.config(function($interpolateProvider)
{
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
});
