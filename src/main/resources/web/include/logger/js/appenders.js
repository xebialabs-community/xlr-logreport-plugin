/*
Copyright 2019 XEBIALABS

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
'use strict';

(function () {
		var LoggerAppenders = function($http, $scope) {

					$scope.loggers =[];
					$scope.loggerMap = [];
					$scope.logLevels = ['OFF', 'DEBUG', 'TRACE', 'INFO', 'WARN', 'ERROR'];
					$scope.submit = function() {
						$http.get('/api/extension/logger/logConfig').then(
							  function success(response) {
							  	$scope.loggers = response['data'];
									$scope.loggerMap = response['data']['entity']['data'];
									console.log($scope.loggerMap);
								}
						);
					};
					$scope.updateAppenderLevel = function(appender, level) {
						console.log(appender);
						console.log(level);
						$http.get('/api/extension/logger/logConfig?verb=SET&logger=' + appender + '&level=' + level).then(
							  function success(response) {
									$scope.loggers = response['data'];
									$scope.loggerMap = response['data']['entity']['data'];
									console.log($scope.loggerMap);
							  },
							  function error(response) {
									console.log(response);
							  });
					};
					$scope.generatecsv = function() {
						$http.get('/api/extension/report?type=' + $scope.selectedValue ).then(
							  function success(response) {
									console.log(response);
							  },
							  function error(response) {
									console.log(response);
							  });

					};
				$scope.submit();
				};

		LoggerAppenders.$inject = ['$http','$scope' ];
		angular.module('extension.logger', []);
		angular.module('extension.logger').controller('xlrelease.logger.LoggerAppenders', LoggerAppenders);
})();
