$(document).ready(function(){
	function initializeDashboard(){
		$.ajax({
			url: 'getGraphicsQE',
			type: 'GET',
			beforeSend: function() {
				console.log('beforeSend')
				$("#loading,#loading-overlay").show();
			},
			complete: function(){
				console.log('complete')
				$("#loading,#loading-overlay").hide();
			},
			success: function(response) {
				console.log('success')
				result = JSON.parse(response);
				if(result.debt_primary_mortgage.success == true){
					console.log('debt_primary_mortgage start')

					Highcharts.chart('debt_primary_mortgage', {
						chart: {
							type: 'column'
						},
						title: {
							text: ''
						},
						xAxis: {
							type: 'debt',
							labels: {
								rotation: -45,
								style: {
									fontSize: '13px',
									fontFamily: 'Verdana, sans-serif'
								}
							}
						},
						yAxis: {
							min: 0,
							title: {
								text: 'Primary Mortgage'
							}
						},
						legend: {
							enabled: false
						},
						tooltip: {
							pointFormat: 'Debts: <b>{point.y:.1f}</b>'
						},
						series: [{
							name: 'Primary Mortgage',
							data: result.debt_primary_mortgage.data,
							dataLabels: {
								enabled: true,
								rotation: -60,
								color: '#FFFFFF',
								align: 'right',
								format: '{point.y:.1f}', // one decimal
								y: 10, // 10 pixels down from the top
								style: {
									fontSize: '13px',
									fontFamily: 'Verdana, sans-serif'
								}
							}
						}]
					});
					console.log('debt_primary_mortgage end')

						Highcharts.chart('debt_household_earners', {
							chart: {
								plotBackgroundColor: null,
								plotBorderWidth: null,
								plotShadow: false,
								type: 'pie'
							},
							title: {
								text: ''
							},
							tooltip: {
								pointFormat: '{series.name}: <b>{point.y}</b>'
							},
							plotOptions: {
								pie: {
									allowPointSelect: true,
									cursor: 'pointer',
									dataLabels: {
										enabled: true,
										format: '<b>{point.name}</b>: {point.percentage:.1f} %',
										style: {
											color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
										}
									}
								}
							},
							series: [{
								name: 'Earners',

								colorByPoint: true,
								data: result.debt_household_earners.data
							}]
						});

						Highcharts.chart('debt_male_female', {
							chart: {
								plotBackgroundColor: null,
								plotBorderWidth: null,
								plotShadow: false,
								type: 'pie'
							},
							title: {
								text: ''
							},
							tooltip: {
								pointFormat: '<b>{point.y}</b>'
							},
							plotOptions: {
								pie: {
									allowPointSelect: true,
									cursor: 'pointer',
									dataLabels: {
										enabled: true,
										format: '<b>{point.name}</b>: {point.percentage:.1f} %',
										style: {
											color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
										}
									}
								}
							},
							series: [{
								name: 'Sex',

								colorByPoint: true,
								data: result.debt_male_female.data
							}]
						});

						Highcharts.chart('debt-student_loan', {
							chart: {
								type: 'column'
							},
							title: {
								text: ''
							},
							xAxis: {
								type: 'debt',
								labels: {
									rotation: -45,
									style: {
										fontSize: '13px',
										fontFamily: 'Verdana, sans-serif'
									}
								}
							},
							yAxis: {
								min: 0,
								title: {
									text: 'Student Loans'
								}
							},
							legend: {
								enabled: false
							},
							tooltip: {
								pointFormat: 'Debts: <b>{point.y:.1f}</b>'
							},
							series: [{
								name: 'Student loans',
								data: result.debt_student_loan.data,
								dataLabels: {
									enabled: true,
									rotation: -60,
									color: '#FFFFFF',
									align: 'right',
									format: '{point.y:.1f}', // one decimal
									y: 10, // 10 pixels down from the top
									style: {
										fontSize: '13px',
										fontFamily: 'Verdana, sans-serif'
									}
								}
							}]
						});

					}

				$("#total_count").text(result.total_count)
				$("#mean").text(result.mean)
				$("#median").text(result.median)
				$("#standard_deviation").text(result.standard_deviation)

				$("#loading,#loading-overlay").hide();
			},
			error: function(error) {
				console.log('error')
				$("#loading,#loading-overlay").hide();
			}
		});
	}
	$("#loading,#loading-overlay").hide();
	initializeDashboard();
});
