//
//  YPAnotherTestApi.swift
//  yupao
//
//  Created by AutoScript on 2023/05/31.
//  Copyright © 2023 AutoScript. All rights reserved.
//

import YPNetKit

public enum YPAnotherTestApi {
	/// 基础价格查询（用于兼容）
	case purchaseIntranetPinInfoPricing(uid: Int, bizType: Int, targetId: Int, preOrderId: Int? = nil, pricingType: Int, topDays: Int, topProvinces: [String], topCities: [String])
	/// 预结算
	case purchaseIntranetPinInfoPreCheckout(uid: Int, bizType: Int, targetId: Int, provinces: [String], cities: [String], days: Int? = nil)
	/// 购买置顶
	case purchaseIntranetPinInfoPurchase(uid: Int, bizType: Int, targetId: Int, provinces: [String], cities: [String], days: Int, approved: Bool, pricingType: Int)
	/// 修改置顶预结算
	case purchaseIntranetPinInfoEditPreCheckout(uid: Int, bizType: Int, targetId: Int, provinces: [String], cities: [String], extendDays: Int, approved: Bool, preOrderId: Int, maxDailyPrice: Int? = nil, totalConsume: String? = nil, notStart: Bool? = nil, endTime: String? = nil, originDays: Int? = nil)
	/// 修改置顶结算
	case purchaseIntranetPinInfoEditPurchase(uid: Int, bizType: Int, targetId: Int, provinces: [String], cities: [String], extendDays: Int, approved: String, preOrderId: Int, maxDailyPrice: Int? = nil, totalConsume: String? = nil, notStart: Bool? = nil, startTime: String? = nil, endTime: String? = nil, originPinTime: String? = nil, pricingType: Int)
}

extension YPAnotherTestApi: YPBaseTargetType {
	public var parameters: [String: Any]? {
		var params: [String: Any] = [:]
		switch self {
		case let .purchaseIntranetPinInfoPricing(uid, bizType, targetId, preOrderId, pricingType, topDays, topProvinces, topCities):
			params["uid"] = uid
			params["bizType"] = bizType
			params["targetId"] = targetId
			params["preOrderId"] = preOrderId
			params["pricingType"] = pricingType
			params["topDays"] = topDays
			params["topProvinces"] = topProvinces
			params["topCities"] = topCities
		case let .purchaseIntranetPinInfoPreCheckout(uid, bizType, targetId, provinces, cities, days):
			params["uid"] = uid
			params["bizType"] = bizType
			params["targetId"] = targetId
			params["provinces"] = provinces
			params["cities"] = cities
			params["days"] = days
		case let .purchaseIntranetPinInfoPurchase(uid, bizType, targetId, provinces, cities, days, approved, pricingType):
			params["uid"] = uid
			params["bizType"] = bizType
			params["targetId"] = targetId
			params["provinces"] = provinces
			params["cities"] = cities
			params["days"] = days
			params["approved"] = approved
			params["pricingType"] = pricingType
		case let .purchaseIntranetPinInfoEditPreCheckout(uid, bizType, targetId, provinces, cities, extendDays, approved, preOrderId, maxDailyPrice, totalConsume, notStart, endTime, originDays):
			params["uid"] = uid
			params["bizType"] = bizType
			params["targetId"] = targetId
			params["provinces"] = provinces
			params["cities"] = cities
			params["extendDays"] = extendDays
			params["approved"] = approved
			params["preOrderId"] = preOrderId
			params["maxDailyPrice"] = maxDailyPrice
			params["totalConsume"] = totalConsume
			params["notStart"] = notStart
			params["endTime"] = endTime
			params["originDays"] = originDays
		case let .purchaseIntranetPinInfoEditPurchase(uid, bizType, targetId, provinces, cities, extendDays, approved, preOrderId, maxDailyPrice, totalConsume, notStart, startTime, endTime, originPinTime, pricingType):
			params["uid"] = uid
			params["bizType"] = bizType
			params["targetId"] = targetId
			params["provinces"] = provinces
			params["cities"] = cities
			params["extendDays"] = extendDays
			params["approved"] = approved
			params["preOrderId"] = preOrderId
			params["maxDailyPrice"] = maxDailyPrice
			params["totalConsume"] = totalConsume
			params["notStart"] = notStart
			params["startTime"] = startTime
			params["endTime"] = endTime
			params["originPinTime"] = originPinTime
			params["pricingType"] = pricingType
		}
		return params
	}

	var path: String {
		switch self {
		case .purchaseIntranetPinInfoPricing:
			return "/purchase/intranet/pinInfo/pricing"
		case .purchaseIntranetPinInfoPreCheckout:
			return "/purchase/intranet/pinInfo/preCheckout"
		case .purchaseIntranetPinInfoPurchase:
			return "/purchase/intranet/pinInfo/purchase"
		case .purchaseIntranetPinInfoEditPreCheckout:
			return "/purchase/intranet/pinInfo/editPreCheckout"
		case .purchaseIntranetPinInfoEditPurchase:
			return "/purchase/intranet/pinInfo/editPurchase"
		}
	}

	var method: Method {
		switch self {
		case .purchaseIntranetPinInfoPricing:
			return .post
		case .purchaseIntranetPinInfoPreCheckout:
			return .post
		case .purchaseIntranetPinInfoPurchase:
			return .post
		case .purchaseIntranetPinInfoEditPreCheckout:
			return .post
		case .purchaseIntranetPinInfoEditPurchase:
			return .post
		}
	}

	var serviceType: ServiceType {
		return .JAVA
	}

	var showLog: Bool {
		return true
	}


}
